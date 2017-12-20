# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .serializer import DeporteSerializer, SucursalSerializer, HorarioxSucursalSerial
from .models import Deporte, Sucursal
from .utils import getsucursalmodel, gethorariosdata, addtipocanchatoserialize


# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class DeporteView(APIView):
    def get(self):
        deporte_model = Deporte.objects.all()
        deporte_serializer = DeporteSerializer(deporte_model, many=True)
        return JSONResponse(deporte_serializer.data)


class SucursalView(APIView):
    def get(self, request):
        if 'id' in request.GET and request.GET['id'] != '':
            sucursal_model = Sucursal.objects.filter(pk=request.GET['id'])
            sucursal_serializer = SucursalSerializer(sucursal_model, many=True)
            data = addtipocanchatoserialize(sucursal_serializer.data, request.GET['id'])
        else:
            sucursal_model = getsucursalmodel(request)
            sucursal_serializer = SucursalSerializer(sucursal_model, many=True)
            data = sucursal_serializer.data
        return JSONResponse(data)


class HorarioxSucursalView(APIView):
    def get(self, request):
        horario_data = gethorariosdata(request)
        horario_serializer = HorarioxSucursalSerial(horario_data, many=True)
        return JSONResponse(horario_serializer.data)
