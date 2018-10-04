from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Empleado, Empresa, Rol

class IndexView(generic.ListView):
    template_name = 'empleados/empleados.html'
    context_object_name = 'empleados_list'

    def get_queryset(self):
        return Empresa.objects.all()
