# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from accounts.models import OCSUser
from .forms import RegisterProductForm
from provider.models import Provider
from .models import Product

def my_products(request):
    u = OCSUser.objects.get(user = request.user)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    return render(request, 'products/my_products.html', {'usuario':u, 'productos':prod,})

def registerProduct(request):
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        register_form = RegisterProductForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(u.id_provider)
            messages.info(request, 'Producto registrado')
            return redirect(reverse('provider:home'))
    else:
        register_form = RegisterProductForm()
    return render(request, 'products/register.html', {'register_form': register_form, 'usuario':u,})

def editProduct(request, id_product):
    u = OCSUser.objects.get(user = request.user)
    p = Product.objects.get(id = id_product)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    return render(request, 'products/edit.html', {'usuario':u,'producto':p,'productos':prod,})

def ableUnableProduct(request, id_product):
    p = Product.objects.get(id = id_product)
    if p.activo:
        p.activo = False
    else:
        p.activo = True
    p.save()
    return editProduct(request, id_product)
