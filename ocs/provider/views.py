# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import proveedor
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


def RegisterView(request):
    return render(request, 'provider/register.html')

def registerProvider(request):
    rfc = request.POST['rfc']
    return 0
