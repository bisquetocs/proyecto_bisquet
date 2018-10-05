from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Empleado, Empresa, Rol
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User



class IndexView(generic.ListView):
    template_name = 'empleados/empleados.html'
    context_object_name = 'empleados_list'

    def get_queryset(self):
        return Empresa.objects.all()

class RegisterView(generic.ListView):
    template_name = 'empleados/reg_empleado.html'
    context_object_name = 'groups_list'

    def get_queryset(self):
        return Group.objects.all()

def vote(request):
    try:
        empleado = User.objects.get(username=request.POST['inputUser'])
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect(reverse('empleados:registro'))
    else:
        return render(request, 'empleados/empleados.html')
