from .models import Sucursal, Horarioatencion, Cancha, Detallereserva
from datetime import datetime
import datetime as dt


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
    canchas_count = Cancha.objects.filter(sucursal=id_sucursal, tipocancha=tipocancha) .count()
    reserva_model = Detallereserva.objects.filter(cancha__sucursal=id_sucursal,
                                                  cancha__tipocancha=tipocancha, reserva__fecha=fecha)
    for ho in horario:
        contador = reserva_model.filter(hora__hour=ho).count()
        if contador < canchas_count:
            horariodisponible.append(ho)
    print horariodisponible
    return horariodisponible


def formathorario(horario):
    data = []
    for ho in horario:
        data.append({'timeinicio': dt.time(ho), 'horainicio': ho})
    return data
