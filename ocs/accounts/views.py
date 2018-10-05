from django.shortcuts import render
from django.contrib.auth.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login



# Create your views here.
def home(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render({}, request))

def logout(request):
    tempate = loader.get_template('registration/logged_out.html')
    return HttpResponse(template.render({}, request))

@login_required
def profile(request):
    current_user = request.user

    return render(request, 'profiles/dashboard.html', {
    ##    'name' : current_user.get_full_name(),
    ##    'rol' : current_user.groups.all()[0]
        })

class EmpleadosView(generic.ListView):
    template_name = 'empleados/empleados.html'
    context_object_name = 'empleados_list'

    def get_queryset(self):
        return User.objects.all()

class RegisterView(generic.ListView):
    template_name = 'empleados/reg_empleado.html'
    context_object_name = 'groups_list'

    def get_queryset(self):
        return Group.objects.all()
def vote(request):
    try:
        usr = request.POST['inputUser']
        employee = User.objects.get(username = usr)
    except (KeyError, User.DoesNotExist):
        return HttpResponseRedirect(reverse('registro'))
    else:
        employee_group = User.groups.through.objects.get(user = employee)
        grp = request.POST['inputRol']
        employee_group.group = Group.objects.get(name = grp)
        employee_group.save()
        return HttpResponseRedirect(reverse('empleados'))
