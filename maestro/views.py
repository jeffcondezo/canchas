# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .serializer import DeporteSerializer, SucursalSerializer, HorarioxSucursalSerial, UsuarioSerializer
from .models import Deporte, Sucursal, Usuario, Detallereserva, Cancha, Reserva
from .forms import AccesoForm
from .utils import getsucursalmodel, gethorariosdata, addtipocanchatoserialize, getsucursalxfechahora, createreserva
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.response import Response

from django.db import IntegrityError

import datetime as dt
# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class RegistroView(APIView):
    def post(self, request):
        user_serializer = UsuarioSerializer(data=request.data)
        if user_serializer.is_valid():
            user_model = User.objects.create_user(user_serializer.initial_data['username'],
                                                  user_serializer.initial_data['email'],
                                                  user_serializer.initial_data['password'])
            user_model.first_name = user_serializer.initial_data['first_name']
            user_model.last_name = user_serializer.initial_data['last_name']
            user_model.save()
            Usuario(celular=user_serializer.initial_data['celular'], user=user_model)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # permission_classes = (AllowAny)
    # Usuario: admin - admin 123456
    def post(self, request):
        form = AccesoForm(request.POST)
        if form.is_valid():
            usuario_form = form.cleaned_data
            user = authenticate(username=usuario_form['username'], password=usuario_form['password'])
            if user is not None:
                if user.is_active:
                    try:
                        token = Token.objects.get(user=user.id)
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=user)
                    response = {"detail": "Autenticacion Correcta.", "token": token.key}
                    return JSONResponse(response)
                else:
                    response = {"detail": "Usuario dado de baja."}
                    return JSONResponse(response)
            else:
                response = {"detail": "Datos de acceso incorrectos."}
                return JSONResponse(response)
        else:
            response = {"detail": form.error_messages}
            return JSONResponse(response)


class LogoutView(APIView):
    def post(self, request):
        token = Token.objects.get(user=request.user)
        usuario = request.user
        token.delete()
        Token.objects.create(user=usuario)
        response = {"detail": "Deslogueo Exitoso."}
        return JSONResponse(response)


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
        elif 'fecha' in request.GET and request.GET['fecha'] != '':
            sucursal_model = getsucursalxfechahora(request)
            sucursal_serializer = SucursalSerializer(sucursal_model, many=True)
            data = sucursal_serializer.data
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


class PreReservaView(APIView):
    def post(self, request):
        response = createreserva(request)
        cancha = Cancha.objects.get(id=1)
        reserva = Reserva.objects.get(id=1)
        detalle_model = Detallereserva(cancha=cancha, hora=dt.time(8), reserva=reserva, codigo='2')
        try:
            detalle_model.save()
            valor = "Wardadito"
        except IntegrityError:
            valor = "Ocupado"
        return JSONResponse({'status': valor})
