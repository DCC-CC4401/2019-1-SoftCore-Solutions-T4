from django.db import models

# Create your models here.

class Rubrica(models.Model):
    nombre = models.CharField(max_length=100)
    #el tipo va a ser un booleano verdadero si es un template y falso si es una instancia
    template = models.BooleanField(default=False)

class Criterio(models.Model):
    #rubrica a la que pertenece
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    #texto es la descripcion del criterio
    texto = models.CharField(max_length=300)

class NivelCumplimiento(models.Model):
    #texto es la descipcion del nivel de cumplimiento
    texto = models.CharField(max_length=300)
    #criterio al que pertenece el nivel
    criterio = models.ForeignKey(Criterio, on_delete=models.CASCADE)
    #valor del puntaje asociado al nivel de cumplimiento
    puntaje = models.FloatField()
    