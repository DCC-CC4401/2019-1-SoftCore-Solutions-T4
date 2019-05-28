from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404


from .models import Evaluacion, Presentacion, Puntaje, LinksResumen

# Create your views here.

class AdminPageView(TemplateView):
    template_name = 'index.html'


def evaluaciones(request):
	evaluaciones_list = Evaluacion.objects.order_by('-fecha_termino')[:5]
	context = {'evaluaciones_list': evaluaciones_list}
	return render(request, 'evaluacion/evaluaciones.html', context)

#TODO 
#def fichaEvaluacion(request, evaluacion_id):
#    evaluacion = get_object_or_404(Evaluacion, pk=evaluacion_id)
#