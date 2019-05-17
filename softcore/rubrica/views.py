from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404


from .models import Rubrica, Criterio, NivelCumplimiento

# Create your views here.


class AdminPageView(TemplateView):
	template_name = 'index.html'

def rubricas(request):
	rubricas_list = Rubrica.objects.order_by('-id')[:6]
	context = {'rubricas_list': rubricas_list}
	return render(request, 'rubrica/rubricas.html', context)

def ficha(request, rubrica_id):
	#NivelCumplimiento.objects.order_by('puntaje')
	rubrica = get_object_or_404(Rubrica, pk=rubrica_id)
	criterios = Criterio.objects.filter(rubrica=rubrica_id)
	max_puntaje = 0
	critKey = criterios.first().id
	for crit in criterios:
		#se sabe que el primer elemento que se saque de NivelCumplimiento es el mayor posible
		temp = NivelCumplimiento.objects.filter(criterio = crit.id).first()
		if(temp.puntaje >= max_puntaje):
			max_puntaje = temp.puntaje
			critKey = crit.id

	niveles = NivelCumplimiento.objects.filter(criterio=critKey)
	return render(request, 'rubrica/ficha_rubrica.html', {'rubrica': rubrica, 'criterios': criterios, 'niveles':niveles})