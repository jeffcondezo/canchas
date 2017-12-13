# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .serializer import DeporteSerializer, SucursalSerializer, HorarioxSucursalSerializer
from .models import Deporte
from .utils import getsucursalmodel, gethorariosmodel, addhorariotoserialize


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
        sucursal_model = getsucursalmodel(request)
        sucursal_serializer = SucursalSerializer(sucursal_model, many=True)
        return JSONResponse(sucursal_serializer.data)


class HorarioxSucursalView(APIView):
    def get(self, request):
        sucursal_model = gethorariosmodel(request)
        horario_serializer = HorarioxSucursalSerializer(sucursal_model, many=True)
        data = addhorariotoserialize(horario_serializer.data, request)
        return JSONResponse(data)
