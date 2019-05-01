from django.db import models
from django.db.models.query_utils import Q

class Rubrica(models.Model):
    tipo = models.CharField(max_length=2)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            # las rubricas template no pueden tener
            # nombres repetidos (pero las instancias si)
            models.UniqueConstraint(
                fields=['nombre'],
                condition=Q(tipo='PL'),
                name='unique_PL_nombre'
            ),
            # las rubricas solo pueden ser de tipo PL o IN
            models.CheckConstraint(check=Q(tipo='PL')|Q(tipo='IN'), name='tipo_PL_IN')
        ]

class Criterio(models.Model):
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    texto = models.CharField(max_length=350)

    def __str__(self):
        return self.texto[:25]

class NivelCumplimiento(models.Model):
    criterio = models.ForeignKey(Criterio, on_delete=models.CASCADE)
    puntaje = models.IntegerField(default=0)
    texto = models.CharField(max_length=350)

    def __str__(self):
        return self.texto[:25]
        