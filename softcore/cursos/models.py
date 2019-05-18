from django.db import models
from django.db.models.query_utils import Q

class Curso(models.Model):
    SEMETRES = (
        # representacion automatica para formularios
        ('O', 'Otoño'),
        ('P', 'Primavera'),
        ('V', 'Verano'),
    )
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=8)
    seccion = models.IntegerField()
    ano = models.IntegerField()
    semestre = models.CharField(max_length=1, choices=SEMETRES)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            # django no permite multiples llaves primarias, asi que usamos unique,
            #  y dejamos que django le asigne id automatico
            models.UniqueConstraint(
                fields=['codigo', 'seccion', 'ano', 'semestre'],
                name='unique_curso'
            ),
            # semestre solo puede ser otoño, primavera o verano
            models.CheckConstraint(
                check=Q(semestre='O')|Q(semestre='P')|Q(semestre='V'),
                name='semestre_O_P_V'
                )
        ]

class Equipo(models.Model):
    # representacion automatica para formularios
    NORMAL_STATE = 'N'
    DISOLVED_STATE = 'D'
    ESTADOS = (
        (DISOLVED_STATE, 'Disuelto'),
        (NORMAL_STATE, 'Normal'),
    )
    nombre = models.CharField(max_length=80)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=1, choices=ESTADOS)

    def __str__(self):
        return self.nombre

    class Meta:
        constraints = [
            # django no permite multiples llaves primarias, asi que usamos unique,
            #  y dejamos que django le asigne id automatico
            models.UniqueConstraint(
                fields=['nombre', 'curso'],
                name='unique_equipo'
            ),
            # semestre solo puede ser otoño, primavera o verano
            models.CheckConstraint(check=Q(estado='D')|Q(estado='N'), name='estado_D_N')
        ]

class Alumno(models.Model):
    # eventualmente el se podría cambiabiar el rut por otro identificador
    #  más conveniente (no sé si los profes pueden extraer el rut de u-cursos)
    rut = models.CharField(max_length=9, primary_key=True)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.SET_NULL,
        limit_choices_to={'estado': Equipo.NORMAL_STATE},
        null=True
    )

    def __str__(self):
        return self.apellidos + ' ' + self.nombres
