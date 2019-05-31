from django.test import TestCase, TransactionTestCase
from django.db import IntegrityError, transaction
from cursos.models import Curso, Equipo, Alumno

class CursosTestCase(TransactionTestCase):
    """Tests para modelos Curso, Equipo, Alumno."""

    def setUp(self):
        try:
            curso1 = Curso.objects.create(nombre='IngenieriaSoftware', codigo='CC1234', seccion=1, ano=2018, semestre='O')
            curso2 = Curso.objects.create(nombre='IngenieriaSoftwareAlias', codigo='CC1234', seccion=2, ano=2018, semestre='O')
            Curso.objects.create(nombre='IngenieriaSoftwareAlias', codigo='CC3333', seccion=2, ano=2018, semestre='O')
            Curso.objects.create(nombre='IngenieriaSoftware', codigo='CC1234', seccion=1, ano=2018, semestre='P')
            Curso.objects.create(nombre='IngenieriaSoftwareAlias', codigo='CC1234', seccion=2, ano=2018, semestre='P')
        except IntegrityError:
            self.fail('Error en setup. En creacion de cursos.')

        try:
            equipo1 = Equipo.objects.create(nombre='softcore', curso=curso1, estado='N')
            equipo2 = Equipo.objects.create(nombre='anotherOne', curso=curso1, estado='N')
            Equipo.objects.create(nombre='softcore', curso=curso2, estado='N')
        except IntegrityError:
            self.fail('Error en setup. En creacion de equipos.')

        try:
            Alumno.objects.create(rut='171231230', nombres='John Junior', apellidos='Doe Smith', equipo=equipo1)
            Alumno.objects.create(rut='17111111k', nombres='Jane Alexandra', apellidos='Doe Smith', equipo=equipo1)
        except IntegrityError:
            self.fail('Error en setup. En creacion de alumnos.')


    def test_semestre_constraint(self):
        """Checkea que el semestre solo sea del tipo otoño (O), primavera(P), o verano (V)."""
        with self.assertRaises(IntegrityError):
            Curso.objects.create(nombre='IngenieriaSoftware', codigo='CC1234', seccion=1, ano=2018, semestre='F')
        with self.assertRaises(IntegrityError):
            Curso.objects.create(nombre='newCurso', codigo='CC7890', seccion=1, ano=2018, semestre='p') # p minúscula

    def test_invalid_curso_insertion(self):
        """Checkea que no se puede insertar un curso repetido (unique_curso constraint)."""
        with self.assertRaises(IntegrityError):
            Curso.objects.create(nombre='AnyName', codigo='CC1234', seccion=2, ano=2018, semestre='O')
        with self.assertRaises(IntegrityError):
            Curso.objects.create(nombre='AnyName', codigo='CC1234', seccion=1, ano=2018, semestre='P')
        with self.assertRaises(IntegrityError):
            Curso.objects.create(nombre='AnyName', codigo='CC1234', seccion=2, ano=2018, semestre='P')

    def test_invalid_equipo_insertion(self):
        """Checkea que no se puede insertar un equipo repetido (unique_equipo constraint)."""
        curso1 = Curso.objects.get(codigo='CC1234', semestre='O', seccion=1)
        with self.assertRaises(IntegrityError):
            Equipo.objects.create(nombre='softcore', curso=curso1, estado='N')
        

    def test_invalid_alumno_insertion(self):
        """Checkea que no se puede insertar un alumno repetido (primary_key constraint)."""
        curso1 = Curso.objects.get(codigo='CC1234', semestre='O', seccion=1)
        equipo1 = Equipo.objects.get(nombre='softcore', curso=curso1)   
        with self.assertRaises(IntegrityError):
            Alumno.objects.create(rut='17111111k', nombres='AnyName', apellidos='AnyLastName', equipo=equipo1)
