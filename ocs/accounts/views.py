from django.shortcuts import render
from django.contrib.auth.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse
from django.db import models







# Create your views here.
def home(request):
    return render(request, 'home/index.html')

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

def register(request):
    return render(request, 'registration/register.html')

def registerUser(request):
    uname = request.POST['username']
    fName = request.POST['firstName']
    lName = request.POST['lastName']
    em = request.POST['email']
    passwd = request.POST['password']
    cpasswd = request.POST['confpass']
    role = request.POST['userRole']

    if (uname==''  or fName=='' or lName=='' or em=='' or passwd=='' or cpasswd=='' or role==''):
        return render(request, 'registration/register.html', {
            'emptyField' : 1
        })

    if (passwd != cpasswd):
        return render(request, 'registration/register.html', {
            'passConfirmError' : 1
        })

    nu = User(username=uname, first_name=fName, last_name=lName, email=em)
    nu.set_password(passwd)
    userTest = User

    # Check if username already exists
    try:
        userTest = User.objects.get(username=nu.username)
    except userTest.DoesNotExist:
        nu.save()
        g = Group.objects.get(name=role)
        g.user_set.add(nu)
        g.save()
        # Redirect to home
        return HttpResponseRedirect('/')
    else:
        # Reload the form if the user already exists
        return render(request, 'registration/register.html', {
            'userAlreadyExists' : 1
        })
