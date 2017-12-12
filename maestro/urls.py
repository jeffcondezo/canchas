# urls.py
from django.conf.urls import url
from .views import DeporteView, SucursalView, HorarioxSucursalView
app_name = 'maestro'
urlpatterns = [
    url(r'^deporte/', DeporteView.as_view()),
    url(r'^sucursal/', SucursalView.as_view()),
    url(r'^horarioxsucursal/', HorarioxSucursalView.as_view()),
]
