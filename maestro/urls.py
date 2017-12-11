# urls.py
from django.conf.urls import url
from .views import DeporteView
app_name = 'maestro'
urlpatterns = [
    url(r'^deporte/', DeporteView.as_view()),
]
