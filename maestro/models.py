# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, connection


# Create your models here.
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


class Cancha(models.Model):
    descripcion = models.CharField(max_length=250)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    tipocancha = models.ForeignKey(Tipocancha, on_delete=models.PROTECT)









