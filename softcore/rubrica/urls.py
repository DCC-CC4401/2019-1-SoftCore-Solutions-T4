from django.urls import path
from . import views

urlpatterns = [
    path('', views.rubricas, name='rubricas'),
    path('<int:rubrica_id>/', views.ficha, name='ficha'),
    path('<int:rubrica_id>/edit/', views.edit_ficha, name='edit_ficha'),
    path('new/', views.new_ficha, name='new_ficha')
]