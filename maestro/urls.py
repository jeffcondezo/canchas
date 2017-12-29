# urls.py
from django.conf.urls import url
from .views import DeporteView, SucursalView, HorarioxSucursalView, \
    RegistroView, LoginView, LogoutView, PreReservaView

app_name = 'maestro'
urlpatterns = [
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
    url(r'^deporte/', DeporteView.as_view()),
    url(r'^sucursal/', SucursalView.as_view()),
    url(r'^horarioxsucursal/', HorarioxSucursalView.as_view()),
    url(r'^registrousuario/', RegistroView.as_view()),
    url(r'^reserva/', PreReservaView.as_view()),
]
