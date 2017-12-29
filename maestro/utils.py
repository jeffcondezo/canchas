from .models import Sucursal, Horarioatencion, Cancha,\
    Detallereserva, Consolidadoreserva, Reserva
from datetime import datetime
import datetime as dt
from .forms import ReservaForm
import string
from django.db import IntegrityError

# SucursalView
def getsucursalxdeporte(id_deporte):
    ids_sucursal = []
    canchas_model = Cancha.objects.filter(tipocancha__subdeporte__deporte=id_deporte).values('sucursal').distinct()
    for cm in canchas_model:
        ids_sucursal.append(cm['sucursal'])
    sucursal_model = Sucursal.objects.filter(pk__in=ids_sucursal)
    return sucursal_model


def getsucursalmodel(request):
    if 'deporte' in request.GET and request.GET['deporte'] != '':
        sucursal_model = getsucursalxdeporte(request.GET['deporte'])
        if 'descripcion' in request.GET and request.GET['descripcion'] != '':
            sucursal_model = sucursal_model.filter(descripcion__icontains=request.GET['descripcion'])
        elif 'latitud' in request.GET and 'longitud' in request.GET:
            latitud = float(request.GET['latitud'])
            longitud = float(request.GET['longitud'])
            ids = Sucursal.objects.in_range(latitud, longitud, 100)
            sucursal_model = sucursal_model.filter(pk__in=ids)
        elif 'distrito' in request.GET and request.GET['distrito'] != '':
            sucursal_model = sucursal_model.filter(distrito=request.GET['distrito'])
    else:
        sucursal_model = Sucursal.objects.none()
    return sucursal_model


def getsucursalxfechahora(request):
    validhours = range(0, 25)
    if 'fecha' in request.GET and request.GET['fecha'] != '':
        try:
            fecha = datetime.strptime(request.GET['fecha'], '%Y-%m-%d')
            if 'horainicio' in request.GET and int(request.GET['horainicio']) in validhours:
                if 'horafin' in request.GET and int(request.GET['horafin']) in validhours:
                    if 'tipocancha' in request.GET and request.GET['tipocancha'] != "":
                        sucursal_model = filtrarsucursaldisponible(getsucursalmodel(request), fecha,
                                                                   request.GET['horainicio'],
                                                                   request.GET['horafin'],
                                                                   request.GET['tipocancha'])
                    else:
                        sucursal_model = Sucursal.objects.none()
                else:
                    sucursal_model = Sucursal.objects.none()
            else:
                sucursal_model = Sucursal.objects.none()
        except ValueError:
            sucursal_model = Sucursal.objects.none()
    return sucursal_model


def filtrarsucursaldisponible(sucursal, fecha, horainicio, horafin, tipocancha):
    horas = range(int(horainicio), int(horafin))
    sucursal_resp = sucursal
    for s in sucursal:
        horario = []
        horarioatencion_model = Horarioatencion.objects.filter(sucursal=s.id, dia__codigo=fecha.weekday())
        for ha in horarioatencion_model:
            horario.extend(range(ha.horainicio.hour, ha.horafin.hour))
        if set(horario).issubset(set(horas)):
            for h in horas:
                try:
                    consolidado_model = Consolidadoreserva.objects.get(fecha=fecha, hora__hour=h,
                                                                       tipocancha=tipocancha)
                    if not consolidado_model.is_libre:
                        sucursal_resp.exclude(id=s.id)
                except Consolidadoreserva.DoesNotExist:
                    pass
        else:
            sucursal_resp.exclude(id=s.id)
        # canchas_count = Cancha.objects.filter(sucursal=s.id, tipocancha=tipocancha).count()
        # for h in horas:
        #     reserva_model = Detallereserva.objects.filter(cancha__sucursal=s.id,
        #                                                   cancha__tipocancha=tipocancha, reserva__fecha=fecha,
        #                                                   hora__hour=h).count()
        #     if canchas_count <= reserva_model:
        #         sucursal_resp.exclude(id=s.id)
    return sucursal_resp


def addtipocanchatoserialize(serialize, id_sucursal):
    if len(serialize) > 0:
        tipo_canchas = []
        canchas_model = Cancha.objects.filter(sucursal=id_sucursal).\
            values('tipocancha', 'tipocancha__descripcion').distinct()
        for cm in canchas_model:
            tipo_canchas.append({'id': cm['tipocancha'], 'descripcion': cm['tipocancha__descripcion']})
        serialize[0].update({'tipocancha': tipo_canchas})
    return serialize


# HorarioxSucursalView
def gethorariosdata(request):
    if 'id' in request.GET and request.GET['id'] != '':
        if 'fecha' in request.GET and request.GET['fecha'] != '':
            if 'tipocancha' in request.GET and request.GET['tipocancha'] != '':
                try:
                    fecha = datetime.strptime(request.GET['fecha'], '%Y-%m-%d')
                    horario = gethorariodisponible(fecha, request.GET['id'], request.GET['tipocancha'])
                    data = formathorario(horario)
                except ValueError:
                    data = []
            else:
                data = []
        else:
            data = []
    else:
        data = []
    return data


def gethorariodisponible(fecha, id_sucursal, tipocancha):
    horario = []
    horariodisponible = []
    horarioatencion_model = Horarioatencion.objects.filter(sucursal=id_sucursal, dia__codigo=fecha.weekday())
    for ha in horarioatencion_model:
        horario.extend(range(ha.horainicio.hour, ha.horafin.hour))
    # canchas_count = Cancha.objects.filter(sucursal=id_sucursal, tipocancha=tipocancha) .count()
    # reserva_model = Detallereserva.objects.filter(cancha__sucursal=id_sucursal,
    #                                               cancha__tipocancha=tipocancha, reserva__fecha=fecha)
    # for ho in horario:
    #     contador = reserva_model.filter(hora__hour=ho).count()
    #     if contador < canchas_count:
    #         horariodisponible.append(ho)
    for ho in horario:
        try:
            consolidado_model = Consolidadoreserva.objects.get(fecha=fecha, hora__hour=ho, tipocancha=tipocancha)
            if consolidado_model.is_libre:
                horariodisponible.append(ho)
        except Consolidadoreserva.DoesNotExist:
            horariodisponible.append(ho)
    return horariodisponible


def formathorario(horario):
    data = []
    for ho in horario:
        data.append({'timeinicio': dt.time(ho), 'horainicio': ho})
    return data


# Reserva
def createreserva(request):
    form = ReservaForm(request.POST)
    if form.is_valid():
        reserva_model = Reserva(fecha=form.cleaned_data['fecha']).save()
        lista_horas = string.split(form.cleaned_data['listahora'], ',')
        fecha = form.cleaned_data['fecha']
        tipocancha = form.cleaned_data['tipocancha']
        idsucursal = form.cleaned_data['idsucursal']
        response = 'Success'
        for lh in lista_horas:
            r = savedetallereserva(fecha, int(lh), tipocancha, reserva_model, idsucursal)
            if r is False:
                response = 'Error'
                break
    else:
        response = 'Error'
    return response


def savedetallereserva(fecha, hora, tipocancha, reserva, idsucursal):
    response = True
    error_count = 0
    for_count = 0
    try:
        consolidado_model = Consolidadoreserva.objects.get(fecha=fecha, hora__hour=hora, tipocancha=tipocancha)
        if consolidado_model.is_libre:
            for cl in string.split(consolidado_model.canchaslibres, ','):
                for_count += 1
                cod_cancha = cl.zfill(6)
                cod_fecha = fecha.strftime('%Y%m%d')
                cod_hora = hora.zfill(2)
                cancha = Cancha.objects.get(id=int(cl))
                detalle_model = Detallereserva(cancha=cancha, hora=dt.time(hora), reserva=reserva,
                                               codigo=cod_cancha+cod_fecha+cod_hora)
                try:
                    detalle_model.save()
                    break
                except IntegrityError:
                    error_count += 1
            if error_count >= for_count:
                response = False
        else:
            response = False
    except Consolidadoreserva.DoesNotExist:
        cancha_model = Cancha.objects.filter(sucursal=idsucursal, tipocancha=tipocancha)
        for c in cancha_model:
            for_count += 1
            detalle_model = Detallereserva(cancha=c, hora=dt.time(hora), reserva=reserva, codigo='2')
            try:
                detalle_model.save()
                break
            except IntegrityError:
                error_count += 1
        if error_count >= for_count:
            response = False
    return response
