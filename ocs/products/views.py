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
from provider.models import Provider
from .models import Product

def my_products(request):
    u = OCSUser.objects.get(user = request.user)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    return render(request, 'products/my_products.html', {'usuario':u, 'productos':prod,})

def registerProduct(request):
    u = OCSUser.objects.get(user = request.user)
    if request.POST['nombre'] == '' or request.POST['descripcion'] == '' or request.POST['codigo'] == '':
        messages.warning(request, 'Necesitas llenar todos los campos!')
    else:
        if request.POST.get('activo', '') == 'on':
            aux = True
        else:
            aux = False
        p = Product(id_provider=u.id_provider,
                        nombre=request.POST['nombre'],
                        descripcion=request.POST['descripcion'],
                        codigo=request.POST['codigo'],
                        activo= aux,
                        fecha_registro=timezone.now())
        p.save()
        messages.success(request, 'Producto registrado!')
    return redirect(reverse('products:myProducts'))

def editProduct(request, id_product):
    u = OCSUser.objects.get(user = request.user)
    p = Product.objects.get(id = id_product)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    if request.method == 'POST':
        if request.POST['nombre'] == '' or request.POST['descripcion'] == '' or request.POST['codigo'] == '':
            messages.warning(request, 'Necesitas llenar todos los campos!')
        else:
            if request.POST.get('activo', '') == 'on':
                aux = True
            else:
                aux = False
            p = Product.objects.get(id=id_product)
            p.nombre=request.POST['nombre']
            p.descripcion=request.POST['descripcion']
            p.codigo=request.POST['codigo']
            p.activo= aux
            p.save()
            messages.success(request, 'La información se actualizó con éxito!')
            return redirect(reverse('products:myProducts'))
    return render(request, 'products/my_products.html', {'usuario':u,'producto':p,'productos':prod,'edit':True})
def ableUnableProduct(request, id_product):
    p = Product.objects.get(id = id_product)
    if p.activo:
        p.activo = False
    else:
        p.activo = True
    p.save()
    return redirect('products:myProducts')
