# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
def deporte_path(instance, filename):
    path = "static/imagenes/deporte/"
    temp = filename.split('.')
    formato = str(instance.id) + '.' + temp[1]
    return path+formato


class Deporte(models.Model):
    descripcion = models.CharField(max_length=250)
    imagen = models.ImageField(upload_to=deporte_path)






