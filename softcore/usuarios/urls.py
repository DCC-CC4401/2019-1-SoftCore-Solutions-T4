from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.evaluadores, name='evaluadores'),
    path('eliminar/<int:pk>/', views.eliminar_evaluador, name='eliminar_evaluador'),
]
