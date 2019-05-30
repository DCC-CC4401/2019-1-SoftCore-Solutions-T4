from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    is_evaluador = models.BooleanField(default=false)
    is_profesor = models.BooleanField(default=false)
    
class Evaluador(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    #todo como extender la password y auth de django ?    
    correo = models.EmailField(primary_key = True)

    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)

class Profesor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    #todo como extender la password y auth de django ?    
    correo = models.EmailField(primary_key = True)

    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)