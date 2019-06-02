from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Evaluador, Profesor

admin.site.register(Evaluador)
admin.site.register(Profesor)