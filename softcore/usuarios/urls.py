from django.urls import path
from . import views

urlpatterns = [
    path('', views.evaluadores, name='evaluadores'),
    #path('new/', views.new_evaluador, name='new_evaluador')
]