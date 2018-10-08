# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import RegisterProductForm

from .models import proveedor

def registerProduct(request):
    if request.method == 'POST':
        register_form = RegisterProductForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration()
            return render(request, 'products/register.html', {'Success_mesage': result})
    else:
        register_form = RegisterProductForm()
    return render(request, 'products/register.html', {'register_form': register_form})
