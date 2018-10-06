from django.shortcuts import render
from django.contrib.auth.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
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
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render({}, request))

def logout(request):
    tempate = loader.get_template('registration/logged_out.html')
    return HttpResponse(template.render({}, request))

@login_required
def profile(request):
    current_user = request.user

    return render(request, 'profiles/dashboard.html', {
        'name' : current_user.get_full_name(),
        'rol' : current_user.groups.all()[0]
        })

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

    nu = User(username=uname, first_name=fName, last_name=lName, email=em)
    nu.set_password(passwd)
    usertest = User
    try:
        usertest = User.objects.get(username=nu.username)
    except usertest.DoesNotExist:
        nu.save()
        g = Group.objects.get(name=role)
        g.user_set.add(nu)
        g.save()

        return HttpResponseRedirect('/')
        # Redireccionar a home
    else:
        return HttpResponse('EL usuario ya existe')
