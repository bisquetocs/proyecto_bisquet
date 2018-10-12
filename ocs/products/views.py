# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from accounts.models import OCSUser
from .forms import RegisterProductForm
from provider.models import Provider
from .models import Product

def registerProduct(request):
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        register_form = RegisterProductForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(u.id_provider)
            return redirect(reverse('provider:home'))
    else:
        register_form = RegisterProductForm()
    return render(request, 'products/register.html', {'register_form': register_form, 'usuario':u,})

def editProduct(request, id_product):
    u = OCSUser.objects.get(user = request.user)
    p = Product.objects.get(id = id_product)
    return render(request, 'products/edit.html', {'usuario':u,'producto':p,})

def ableUnableProduct(request, id_product):
    p = Product.objects.get(id = id_product)
    if p.activo:
        p.activo = False
    else:
        p.activo = True
    p.save()
    return editProduct(request, id_product)
