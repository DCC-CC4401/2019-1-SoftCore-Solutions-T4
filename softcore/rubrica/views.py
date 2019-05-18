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
	rubrica = get_object_or_404(Rubrica, pk=rubrica_id)
	criterios = Criterio.objects.filter(rubrica=rubrica_id)
	max_puntaje = 0
	critKey = criterios.first().id
	#aca se buscan todos los niveles de aprobacion
	for crit in criterios:
		#se sabe que el primer elemento que se saque de NivelCumplimiento es el mayor posible
		temp = NivelCumplimiento.objects.filter(criterio = crit.id).first()
		if(temp.puntaje >= max_puntaje):
			max_puntaje = temp.puntaje
			critKey = crit.id

	niveles = NivelCumplimiento.objects.filter(criterio=critKey)
	#el contexto lleva la rubrica en cuestion, un set de niveles que es la primera file de la tabla
	#ademas de los criterios a partir de los cuales se contruye el resto de la tabla
	#de esta forma el manejo de la contruccion en el template es mas limpio
	return render(request, 'rubrica/ficha_rubrica.html', {'rubrica': rubrica, 'criterios': criterios, 'niveles':niveles})

def edit_ficha(request, rubrica_id):
	rubrica = get_object_or_404(Rubrica, pk=rubrica_id)
	criterios = Criterio.objects.filter(rubrica=rubrica_id)
	max_puntaje = 0
	critKey = criterios.first().id
	#aca se buscan todos los niveles de aprobacion
	for crit in criterios:
		#se sabe que el primer elemento que se saque de NivelCumplimiento es el mayor posible
		temp = NivelCumplimiento.objects.filter(criterio = crit.id).first()
		if(temp.puntaje >= max_puntaje):
			max_puntaje = temp.puntaje
			critKey = crit.id

	niveles = NivelCumplimiento.objects.filter(criterio=critKey)
	#el contexto lleva la rubrica en cuestion, un set de niveles que es la primera file de la tabla
	#ademas de los criterios a partir de los cuales se contruye el resto de la tabla
	#de esta forma el manejo de la contruccion en el template es mas limpio
	return render(request, 'rubrica/edit_ficha.html', {'rubrica': rubrica, 'criterios': criterios, 'niveles':niveles})

def new_ficha(request):
	return render(request, 'rubrica/new_ficha.html', None)