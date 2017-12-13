from .models import Sucursal, Horarioatencion, Cancha
from datetime import datetime


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
            sucursal_model = sucursal_model.filter(descripcion__contains=request.GET['descripcion'])
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


# HorarioxSucursalView
def gethorariosmodel(request):
    if 'id' in request.GET and request.GET['id'] != '':
        sucursal_model = Sucursal.objects.filter(pk=request.GET['id'])
    else:
        sucursal_model = Sucursal.objects.none()
    return sucursal_model


def addhorariotoserialize(serialize, request):
    if len(serialize) > 0:
        if 'fecha' in request.GET and request.GET['fecha'] != '':
            try:
                fecha = datetime.strptime(request.GET['fecha'], '%Y-%m-%d')
                horario = gethorariodisponible(fecha.weekday(), request.GET['id'])
                serialize[0].update({'horario': horario})
            except ValueError:
                serialize[0].update({'horario': []})
        else:
            serialize[0].update({'horario': []})
    return serialize


def gethorariodisponible(weekday, id_sucursal):
    horario = []
    horarioatencion_model = Horarioatencion.objects.filter(sucursal=id_sucursal, dia__codigo=weekday)
    for ha in horarioatencion_model:
        horario.extend(range(ha.horainicio.hour, ha.horafin.hour))
    return horario
