from django.db import models
from django.conf import settings

from cursos.models import Curso, Equipo, Alumno
from rubrica.models import Rubrica, Criterio, NivelCumplimiento

class Evaluacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    duracion_min = models.DurationField()
    duracion_max = models.DurationField()
    rubrica = models.ForeignKey(Rubrica, on_delete=models.SET_NULL, null=True)
    evaluadores = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            # django no permite multiples llaves primarias, asi que usamos unique,
            #  y dejamos que django le asigne id automatico
            models.UniqueConstraint(
                fields=['nombre', 'curso'],
                name='unique_evaluacion'
            ),
        ]

class Presentacion(models.Model): # evaluacion equipo
    evaluador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    snapshot_equipo = models.ManyToManyField(Alumno, related_name='alumnos_snapshot')
    presentadores = models.ManyToManyField(Alumno, related_name='alumnos_presentadores')

    def __str__(self):
        return 'Presentacion: ' + self.equipo + ' en ' + self.evaluacion

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['evaluacion', 'equipo'],
                name='unique_presentacion'
            ),
        ]

class Puntaje(models.Model): # nivel cumplimiento x evaluacion equipo
    criterio = models.ForeignKey(Criterio, on_delete=models.CASCADE)
    nivel_cumplimiento = models.ForeignKey(NivelCumplimiento, on_delete=models.CASCADE, related_name='cumplimiento_criterio')
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)

    def __str__(self):
        return 'Puntaje: ' + self.nivel_cumplimiento.puntaje + '. Id: ' + self.id

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['criterio', 'presentacion'],
                name='unique_puntaje'
            ),
        ]

class LinksResumen(models.Model):
    url = models.CharField(max_length=100, primary_key=True)
    contraseña = models.CharField(max_length=50) # ver tema de encryptación?
    evaluacion = models.ForeignKey(Evaluacion, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    def __str__(self):
        return 'Link_' + self.equipo + '_' + self.evaluacion

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['evaluacion', 'equipo'],
                name='unique_evaluacion_equipo'
            ),
        ]

