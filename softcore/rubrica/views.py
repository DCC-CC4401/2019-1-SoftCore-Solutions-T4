from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
import json as json


from .models import Rubrica, Criterio, NivelCumplimiento

# Create your views here.


class AdminPageView(TemplateView):
	template_name = 'index.html'

def rubricas(request):
	if request.method == "POST":
		rubricaId = int(request.POST['id'])
		rubrica = get_object_or_404(Rubrica, pk=rubricaId)
		rubrica.delete()
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
	error = False
	if request.method == "POST":
		data = json.loads(request.body)
		rubricasWithName = Rubrica.objects.filter(nombre=data['nombre'])
		if(len(rubricasWithName) == 0 or rubricasWithName[0].id == data['id']):
			
			rubrica = get_object_or_404(Rubrica, pk=int(data['id']))
			rubrica.delete()
			rubrica = Rubrica()
			rubrica.id = int(data['id'])
			rubrica.nombre = data['nombre']
			rubrica.tipo = "PL"
			rubrica.save()

			puntajes=data['filas'][0]

			for fila in data['filas'][1:]:
				nuevoCrit = Criterio()
				nuevoCrit.rubrica = rubrica
				nuevoCrit.texto = fila[0]
				nuevoCrit.save()
				for i in range(1,len(fila)):
					nuevoNivel = NivelCumplimiento(criterio=nuevoCrit, texto=fila[i], puntaje=int(puntajes[i]))
					nuevoNivel.save()

		else:
			error = True

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
	return render(request, 'rubrica/edit_ficha.html', {'rubrica': rubrica, 'criterios': criterios, 'niveles':niveles, 'error': False, 'rubricas': Rubrica.objects.all()})

def new_ficha(request):
	if request.method == "POST":
		data = json.loads(request.body)
		rubricasWithName = Rubrica.objects.filter(nombre=data['nombre'])
		if(len(rubricasWithName) == 0):
			newRubrica = Rubrica(tipo="PL", nombre=data['nombre'])
			newRubrica.save()
		
			puntajes=data['filas'][0]

			for fila in data['filas'][1:]:
				nuevoCrit = Criterio()
				nuevoCrit.rubrica = newRubrica
				nuevoCrit.texto = fila[0]
				nuevoCrit.save()
				for i in range(1,len(fila)):
					nuevoNivel = NivelCumplimiento(criterio=nuevoCrit, texto=fila[i], puntaje=int(puntajes[i]))
					nuevoNivel.save()
		return render(request, 'rubrica/new_ficha.html', {'rubricas': Rubrica.objects.all()})
	else:
		return render(request, 'rubrica/new_ficha.html', {'rubricas': Rubrica.objects.all()})

def save_ficha(request, rubrica_id=None):
		print("hola llego un post, creo")
	#if(request.method == 'POST'):