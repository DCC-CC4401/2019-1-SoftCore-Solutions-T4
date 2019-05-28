from django.contrib import admin

from .models import Evaluacion, Presentacion, Puntaje, LinksResumen

admin.site.register(Evaluacion)
admin.site.register(Presentacion)
admin.site.register(Puntaje)
admin.site.register(LinksResumen)

# Register your models here.
