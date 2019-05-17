from django.urls import path
from . import views

urlpatterns = [
    path('', views.rubricas, name='rubricas'),
    path('<int:rubrica_id>/', views.ficha, name='ficha'),
]