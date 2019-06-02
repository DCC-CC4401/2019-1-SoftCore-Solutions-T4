from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404


from .models import CustomUser
# Create your views here.


class AdminPageView(TemplateView):
    template_name = 'index.html'


def evaluadores(request):
    if request.method == 'POST':
        username = request.POST['username']
        apellido = request.POST['apellido']
        email = request.POST['email']
        tipo_usuario = request.POST['tipo_usuario']

        if tipo_usuario == 'profesor':
            CustomUser.objects.create(correo=email, nombre=username,
                                      apellido=apellido, profesor=True)
        else:
            CustomUser.objects.create(correo=email, nombre=username,
                                      apellido=apellido, evaluador=True)

    evaluadores_list = CustomUser.objects.all()
    context = {'evaluadores_list': evaluadores_list}
    return render(request, 'usuarios/evaluadores1.html', context)
