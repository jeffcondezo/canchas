from .models import Sucursal


def getsucursalmodel(request):
    if 'descripcion' in request.GET and request.GET['descripcion'] != '':
        sucursal_model = Sucursal.objects.filter(descripcion__contains=request.GET['descripcion'])
    elif 'latitud' in request.GET and 'longitud' in request.GET:
        latitud = float(request.GET['latitud'])
        longitud = float(request.GET['longitud'])
        ids = Sucursal.objects.in_range(latitud, longitud, 100)
        sucursal_model = Sucursal.objects.filter(pk__in=ids)
    elif 'distrito' in request.GET and request.GET['distrito'] != '':
        sucursal_model = Sucursal.objects.filter(distrito=request.GET['distrito'])
    else:
        sucursal_model = Sucursal.objects.all()
    return sucursal_model


def gethorariosmodel(request):
    if 'id' in request.GET and request.GET['id'] != '':
        sucursal_model = Sucursal.objects.filter(pk=request.GET['id'])
    else:
        sucursal_model = Sucursal.objects.none()
    return sucursal_model
