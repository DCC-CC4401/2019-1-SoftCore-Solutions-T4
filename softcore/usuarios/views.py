from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404


from .models import Evaluador
# Create your views here.

class AdminPageView(TemplateView):
	template_name = 'index.html'

def evaluadores(request):
	evaluadores_list = Evaluador.objects.all()
	context = {'evaluadores_list': evaluadores_list}
	return render(request, 'usuarios/evaluadores.html', context)
