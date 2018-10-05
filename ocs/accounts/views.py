from django.shortcuts import render
from django.contrib.auth.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
        'name' : current_user.get_full_name(),
        'rol' : current_user.groups.all()[0]
        })
