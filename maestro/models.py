# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    celular = models.CharField(max_length=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usuario')
    is_encargado = models.BooleanField(default=False)


class Departamento(models.Model):
    descripcion = models.CharField(max_length=250)


class Provincia(models.Model):
    descripcion = models.CharField(max_length=250)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)


class Distrito(models.Model):
    descripcion = models.CharField(max_length=250)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    def __unicode__(self):
        return '%s' % self.descripcion


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
    deporte = models.ForeignKey(Deporte, on_delete=models.PROTECT)


class Tipocancha(models.Model):
    descripcion = models.CharField(max_length=250)
    subdeporte = models.ForeignKey(Subdeporte, on_delete=models.PROTECT)


def empresa_path(instance, filename):
    path = "static/imagenes/empresa/"
    temp = filename.split('.')
    formato = str(instance.ruc) + '.' + temp[1]
    return path+formato


class Empresa(models.Model):
    descripcion = models.CharField(max_length=250)
    ruc = models.CharField(max_length=11)
    imagen = models.ImageField(upload_to=empresa_path)


class LocationManager(models.Manager):
    def in_range(self, latitude, longitude, radius, results=100):
        unit = 6371  # Distance unit (kms)
        radius = float(radius) / 1000.0  # Distance radius convert m to km
        latitude = float(latitude)  # Central point latitude
        longitude = float(longitude)  # Central point longitude

        sql = """SELECT id FROM
                    (SELECT id, latitud, longitud, ({unit} * acos(CAST((cos(radians({latitude})) * cos(radians(latitud))
                     *cos(radians(longitud) - radians({longitude})) + sin(radians({latitude})) * 
                     sin(radians(latitud))) AS DECIMAL))) AS distance
                     FROM maestro_sucursal) AS distances
                 WHERE distance < {radius}
                 ORDER BY distance
                 OFFSET 0
                 LIMIT {results};""".format(unit=unit, latitude=latitude, longitude=longitude, radius=radius,
                                            results=results)

        cursor = connection.cursor()
        cursor.execute(sql)
        ids = [row[0] for row in cursor.fetchall()]
        return ids


class Sucursal(models.Model):
    descripcion = models.CharField(max_length=250)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=250)
    latitud = models.FloatField()
    longitud = models.FloatField()

    objects = LocationManager()


class Encargado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    is_activo = models.BooleanField()


class Dia(models.Model):
    descripcion = models.CharField(max_length=250)
    codigo = models.SmallIntegerField()


class Horarioatencion(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    dia = models.ForeignKey(Dia, on_delete=models.PROTECT)
    horainicio = models.TimeField()
    horafin = models.TimeField()


class Cancha(models.Model):
    descripcion = models.CharField(max_length=250)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tipocancha = models.ForeignKey(Tipocancha, on_delete=models.PROTECT)


class Reserva(models.Model):
    fecha = models.DateField()
    is_pagado = models.BooleanField(default=False)


class Detallereserva(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.PROTECT)
    hora = models.TimeField()
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=14, unique=True, null=True, blank=True)


class Consolidadoreserva(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    canchasocupadas = models.CharField(max_length=150, blank=True, null=True)
    canchaslibres = models.CharField(max_length=150, blank=True, null=True)
    tipocancha = models.ForeignKey(Tipocancha, on_delete=models.PROTECT)
    is_libre = models.BooleanField(default=True)
