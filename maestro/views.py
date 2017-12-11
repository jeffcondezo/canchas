# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .serializer import DeporteSerializer
from .models import Deporte


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
    def get(self, request):
        servicio_model = Deporte.objects.all()
        servicio_serializer = DeporteSerializer(servicio_model, many=True)
        return JSONResponse(servicio_serializer.data)
