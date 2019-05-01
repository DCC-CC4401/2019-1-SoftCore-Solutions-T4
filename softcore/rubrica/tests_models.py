from django.test import TestCase
from django.db import Error
from rubrica.models import Rubrica, Criterio, NivelCumplimiento

CRIT_PL_TEXT = 'criterio rub plantilla'
CRIT_IN_TEXT = 'criterio rub instancia'
NIV_PL_TEXT = 'nivel cumplimiento plantilla'
NIV_IN_TEXT = 'nivel cumplimiento instancia'
TEST_RUB = 'testRub'
PL = 'PL'
IN = 'IN'

class RubricaTestCase(TestCase):
    """Tests para modelos de las rubricas, criterios y niveles de cumplimiento."""

    def setUp(self):
        plantilla = Rubrica.objects.create(nombre=TEST_RUB, tipo=PL)
        instancia = Rubrica.objects.create(nombre=TEST_RUB, tipo=IN)
        crit_pl = Criterio.objects.create(rubrica=plantilla, texto=CRIT_PL_TEXT)
        crit_in = Criterio.objects.create(rubrica=instancia, texto=CRIT_IN_TEXT)
        NivelCumplimiento.objects.create(criterio=crit_pl, puntaje=5, texto=NIV_PL_TEXT)
        NivelCumplimiento.objects.create(criterio=crit_in, puntaje=6, texto=NIV_IN_TEXT)

    def test_invalid_insert(self):
        """Checkea que solo se puede insertar rubricas de tipo PL e IN."""
        with self.assertRaises(Error):
            Rubrica.objects.create(nombre=TEST_RUB, tipo='Invalid')

    def test_pl_duplicate(self):
        """Checkea que solo puede insertarse una rubrica plantilla con el mismo nombre."""
        with self.assertRaises(Error):
            Rubrica.objects.create(nombre=TEST_RUB, tipo=PL)

    def test_in_duplicate(self):
        """Checkea que si se puede insertar mas de una rubrica instancia con el mismo nombre."""
        try:
            Rubrica.objects.create(nombre=TEST_RUB, tipo=IN)
        except Error:
            self.fail('Rubricas de tipo instancia deben poder tener nombres repetidos.')

    def test_get_crits_nivs(self):
        """Comprueba la consistencia basica de los datos. En particular comprueba
        que las consultas intuitivas para obtener los criterios de una rubrica y el
        nivel de cumplimiento de un criterio funcionan."""
        rub_pl = Rubrica.objects.get(nombre=TEST_RUB, tipo=PL)
        rub_in = Rubrica.objects.get(nombre=TEST_RUB, tipo=IN)

        crit_pl = Criterio.objects.get(id=rub_pl.id)
        self.assertEqual(crit_pl.texto, CRIT_PL_TEXT)

        crit_in = Criterio.objects.get(rubrica__id=rub_in.id)
        self.assertEqual(crit_in.texto, CRIT_IN_TEXT)

        niv_pl = NivelCumplimiento.objects.get(criterio__rubrica__id=rub_pl.id)
        self.assertEqual(niv_pl.texto, NIV_PL_TEXT)

        niv_in = NivelCumplimiento.objects.get(criterio__rubrica__id=rub_in.id)
        self.assertEqual(niv_in.texto, NIV_IN_TEXT)
                