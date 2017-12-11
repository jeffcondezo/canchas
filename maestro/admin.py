# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin


# Register your models here.
from .models import Deporte, Subdeporte, Tipocancha, Empresa, Cancha, Sucursal\
    , Departamento, Provincia, Distrito

admin.site.register(Deporte)
admin.site.register(Subdeporte)
admin.site.register(Tipocancha)
admin.site.register(Empresa)
admin.site.register(Cancha)
admin.site.register(Sucursal)
admin.site.register(Departamento)
admin.site.register(Provincia)
admin.site.register(Distrito)
