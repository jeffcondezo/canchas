# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Departamento(models.Model):
    descripcion = models.CharField(max_length=250)


class Provincia(models.Model):
    descripcion = models.CharField(max_length=250)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)


class Distrito(models.Model):
    descripcion = models.CharField(max_length=250)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)


# Create your models here.
def deporte_path(instance, filename):
    path = "static/imagenes/deporte/"
    temp = filename.split('.')
    formato = str(instance.descripcion) + '.' + temp[1]
    return path+formato


class Deporte(models.Model):
    descripcion = models.CharField(max_length=250)
    imagen = models.ImageField(upload_to=deporte_path)


class Subdeporte(models.Model):
    descripcion = models.CharField(max_length=250)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)


class Tipocancha(models.Model):
    descripcion = models.CharField(max_length=250)


def empresa_path(instance, filename):
    path = "static/imagenes/empresa/"
    temp = filename.split('.')
    formato = str(instance.ruc) + '.' + temp[1]
    return path+formato


class Empresa(models.Model):
    descripcion = models.CharField(max_length=250)
    ruc = models.CharField(max_length=11)
    imagen = models.ImageField(upload_to=empresa_path)


class Sucursal(models.Model):
    descripcion = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=250)
    latitud = models.CharField(max_length=15)
    longitud = models.CharField(max_length=15)


class Cancha(models.Model):
    descripcion = models.CharField(max_length=250)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tipocancha = models.ForeignKey(Tipocancha, on_delete=models.PROTECT)









