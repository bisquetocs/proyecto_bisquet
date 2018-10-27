"""
created by:     Django
description:    This are the views used to work with products
modify by:      Alberto
modify date:    26/10/18
"""
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

# Function that shows the provider its products
def my_products(request):
    u = OCSUser.objects.get(user = request.user)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    return render(request, 'products/my_products.html', {'usuario':u, 'productos':prod,})

# Function that let the provider register a new product
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
                        nombre=request.POST['nombre'].lower(),
                        descripcion=request.POST['descripcion'],
                        codigo=(request.POST['codigo']).upper(),
                        activo= aux,
                        fecha_registro=timezone.now())
        prod1 = Product.objects.filter(nombre=p.nombre, id_provider=p.id_provider)
        prod2 = Product.objects.filter(codigo=p.codigo, id_provider=p.id_provider)
        if not prod1 and not prod2:
            p.save()
            messages.success(request, 'Producto registrado!')
        else:
            if prod1 and prod2:
                messages.warning(request, 'El nombre y el código asignados ya existen')
            elif prod2:
                messages.warning(request, 'El código asignado ya existe')
            else:
                messages.warning(request, 'El nombre asignado ya existe')
    return redirect(reverse('products:myProducts'))

# Function that lest the provider to edit its products
def editProduct(request, id_product):
    u = OCSUser.objects.get(user = request.user)
    p = Product.objects.get(id = id_product)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    # If POST then make validations and save product info
    if request.method == 'POST':
        if request.POST['nombre'] == '' or request.POST['descripcion'] == '' or request.POST['codigo'] == '':
            messages.warning(request, 'Necesitas llenar todos los campos!')
        else:
            if request.POST.get('activo', '') == 'on':aux = True
            else:aux = False
            p = Product.objects.get(id=id_product)
            prod1 = Product.objects.filter(nombre=request.POST['nombre'].lower(), id_provider=p.id_provider).exclude(id=id_product)
            prod2 = Product.objects.filter(codigo=request.POST['codigo'].upper(), id_provider=p.id_provider).exclude(id=id_product)
            if not prod1 and not prod2:
                p.nombre=request.POST['nombre'].capitalize()
                p.descripcion=request.POST['descripcion']
                p.codigo=request.POST['codigo'].upper()
                p.activo= aux
                p.save()
                messages.success(request, 'La información se actualizó con éxito!')
                return redirect(reverse('products:myProducts'))
            else:
                auxp = Product(id=p.id,
                                id_provider=u.id_provider,
                                nombre=request.POST['nombre'],
                                descripcion=request.POST['descripcion'],
                                codigo=request.POST['codigo'],
                                activo= aux)
                if prod1 and prod2:
                    messages.warning(request, 'El nombre y el código asignados ya existen')
                    auxp.nombre = ''
                    auxp.codigo = ''
                elif prod2:
                    messages.warning(request, 'El código asignado ya existe')
                    auxp.codigo = ''
                else:
                    messages.warning(request, 'El nombre asignado ya existe')
                    auxp.nombre = ''
                return render(request, 'products/my_products.html', {'usuario':u,'producto':auxp,'productos':prod,'edit':True})
    return render(request, 'products/my_products.html', {'usuario':u,'producto':p,'productos':prod,'edit':True})

# Function that lets the provider rapidly unable a product
def ableUnableProduct(request, id_product):
    p = Product.objects.get(id = id_product)
    if p.activo:
        p.activo = False
    else:
        p.activo = True
    p.save()
    return redirect('products:myProducts')
