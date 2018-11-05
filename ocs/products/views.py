"""
created by:     Django
description:    This are the views used to work with products
modify by:      Alberto
modify date:    04/11/18
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
from .models import UnidadDeMedida
from .models import Price
from .models import CompleteProduct
from .models import Equivalencias

from django.http import JsonResponse
import json


# INPUT
# OUTPUT
# Function that shows the provider its products
def my_products(request):
    u = OCSUser.objects.get(user = request.user)
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id).order_by('-id')
    unidad = UnidadDeMedida.objects.all()
    return render(request, 'products/my_products.html', {'usuario':u, 'productos':prod,'unidad':unidad,})

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
            if request.POST['precio']!=0 and request.POST.get('unidad_medida',0)!=0:
                unidad = UnidadDeMedida.objects.get(id=request.POST['unidad_medida'])
                price = Price(id_product = p,fecha_inicio = timezone.now(), cantidad = request.POST['precio'], activo = True)
                price.save()
                complete = CompleteProduct(id_product=p, id_unidad=unidad, id_price=price, activo=True)
                complete.save()
            messages.success(request, 'Producto registrado!')
        else:
            if prod1 and prod2:
                messages.warning(request, 'El nombre y el código asignados ya existen')
            elif prod2:
                messages.warning(request, 'El código asignado ya existe')
            else:
                messages.warning(request, 'El nombre asignado ya existe')
    return redirect(reverse('products:myProducts'))


# AJAX FUNCTIONS
def able_unable_product(request):
    id_product = request.GET.get('id_product', None)
    p = Product.objects.get(id = id_product)
    if p.activo:
        p.activo = False
    else:
        p.activo = True
    p.save()
    data = {
        'able': p.activo,
    }
    return JsonResponse(data)
def get_product_info(request):
    id_product = request.GET.get('id_product', None)
    product = Product.objects.get(id=id_product)
    data = {
        'id_product': product.id,
        'nombre': product.nombre,
        'descripcion': product.descripcion,
        'codigo': product.codigo,
        'activo': product.activo,
    }
    return JsonResponse(data)
def edit_product(request):
    u = OCSUser.objects.get(user = request.user)
    p = Product.objects.get(id = request.POST['id_product'])
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    # If POST then make validations and save product info
    if request.method == 'POST':
        if request.POST['nombre'] == '' or request.POST['descripcion'] == '' or request.POST['codigo'] == '':
            messages.warning(request, 'Necesitas llenar todos los campos!')
        else:
            if request.POST.get('activo', '') == 'on':aux = True
            else:aux = False
            p = Product.objects.get(id=request.POST['id_product'])
            prod1 = Product.objects.filter(nombre=request.POST['nombre'].lower(), id_provider=p.id_provider).exclude(id=request.POST['id_product'])
            prod2 = Product.objects.filter(codigo=request.POST['codigo'].upper(), id_provider=p.id_provider).exclude(id=request.POST['id_product'])
            if not prod1 and not prod2:
                p.nombre=request.POST['nombre'].lower()
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
def get_product_price(request):
    id_product = request.GET.get('id_product', None)
    product = Product.objects.get(id=id_product)
    complete = CompleteProduct.objects.filter(id_product = product, activo=True, id_price__in = Price.objects.filter(id_product=product,activo=True))
    complete = complete.order_by('id_unidad')
    data = {
        'id_product': id_product,
        'id_unidad': [],
        'id_precio': [],
        'unidad': [],
        'precio': [],
    }
    for comp in complete:
        data['id_unidad'].append(comp.id_unidad.id)
        data['id_precio'].append(comp.id_price.id)
        data['unidad'].append(UnidadDeMedida.objects.get(id=comp.id_unidad.id).abreviacion + ' - ' + UnidadDeMedida.objects.get(id=comp.id_unidad.id).nombre)
        data['precio'].append(Price.objects.get(id=comp.id_price.id).cantidad)
    return JsonResponse(data)

def check_unidad(request):
    id_product = request.GET.get('id_product', None)
    product = Product.objects.get(id=id_product)
    unidadesTotal = UnidadDeMedida.objects.all()
    unidades = CompleteProduct.objects.filter(id_product=product, activo = True)
    data = {
        'id_product': id_product,
        'unidadesTotal': [],
        'unidades': [],
    }
    for uni in unidadesTotal:
        data['unidadesTotal'].append(uni.id)
    for uni in unidades:
        data['unidades'].append(uni.id_unidad.id)
    print(data)
    return JsonResponse(data)

def add_price(request):
    id_product = request.GET.get('id_product', None)
    id_unidad = request.GET.get('id_unidad', None)
    cantidad = request.GET.get('cantidad', None)
    product = Product.objects.get(id=id_product)
    unidad = UnidadDeMedida.objects.get(id=id_unidad)
    price = Price(id_product=product, fecha_inicio = timezone.now(),cantidad = cantidad, activo=True)
    price.save()
    complete = CompleteProduct(id_product=product,id_unidad=unidad,id_price=price,activo=True)
    complete.save()
    data = { 'success': True,}
    return JsonResponse(data)
def save_price(request):
    id_product = request.GET.get('id_product', None)
    id_unidad = request.GET.get('id_unidad', None)
    cantidad = request.GET.get('cantidad', None)
    product = Product.objects.get(id=id_product)
    unidad = UnidadDeMedida.objects.get(id=id_unidad)
    complete = CompleteProduct.objects.get(id_product=product,id_unidad=unidad,activo=True)
    price = Price.objects.get(id = complete.id_price.id)
    price.fecha_final = timezone.now()
    price.activo = False
    price.save()
    newPrice = Price(id_product=product, fecha_inicio=timezone.now(), cantidad=cantidad, activo=True)
    newPrice.save()
    complete.id_price = newPrice
    complete.save()
    data = { 'success': True,}
    return JsonResponse(data)
def delete_price(request):
    id_product = request.GET.get('id_product', None)
    id_unidad = request.GET.get('id_unidad', None)
    product = Product.objects.get(id=id_product)
    unidad = UnidadDeMedida.objects.get(id=id_unidad)
    complete = CompleteProduct.objects.get(id_product=product,id_unidad=unidad,activo=True)
    price = Price.objects.get(id = complete.id_price.id)
    price.fecha_final = timezone.now()
    price.activo = False
    complete.activo = False
    price.save()
    complete.save()
    data = { 'success': True,}
    return JsonResponse(data)






def get_product_equiv(request):
    id_product = request.GET.get('id_product', None)
    product = Product.objects.get(id=id_product)
    equiv = Equivalencias.objects.filter(id_product = product, activo=True).order_by('id_unidad_origen')
    data = {
        'id_equiv': [],
        'id_unidad_origen': [],
        'cantidad_origen': [],
        'id_unidad_destino': [],
        'cantidad_destino': [],
    }
    print(equiv)
    for equi in equiv:
        data['id_equiv'].append(equi.id)
        data['id_unidad_origen'].append(equi.id_unidad_origen.abreviacion)
        data['cantidad_origen'].append(equi.cantidad_origen)
        data['id_unidad_destino'].append(equi.id_unidad_destino.abreviacion)
        data['cantidad_destino'].append(equi.cantidad_destino)
    return JsonResponse(data)

def add_equivalencia(request):
    id_product = request.GET.get('id_product', None)
    id_unidad_origen = request.GET.get('id_unidad_origen', None)
    cantidad_origen = request.GET.get('cantidad_origen', None)
    id_unidad_destino = request.GET.get('id_unidad_destino', None)
    cantidad_destino = request.GET.get('cantidad_destino', None)

    product = Product.objects.get(id=id_product)
    unidad_origen = UnidadDeMedida.objects.get(id=id_unidad_origen)
    unidad_destino = UnidadDeMedida.objects.get(id=id_unidad_destino)

    exist = Equivalencias.objects.filter(id_product=product, id_unidad_origen=unidad_origen, id_unidad_destino=unidad_destino, activo=True).exists()
    if exist:
        equiv = Equivalencias.objects.get(id_product=product, id_unidad_origen=unidad_origen, id_unidad_destino=unidad_destino, activo=True)
        equiv.cantidad_origen = cantidad_origen
        equiv.cantidad_destino = cantidad_destino
        equiv.save()
    else:
        equiv = Equivalencias(id_product=product, id_unidad_origen=unidad_origen, cantidad_origen=cantidad_origen, id_unidad_destino=unidad_destino, cantidad_destino=cantidad_destino, activo=True)
        equiv.save()
    data = { 'unidad_origen': unidad_origen.abreviacion,
                'cantidad_origen': cantidad_origen,
                'unidad_destino': unidad_destino.abreviacion,
                'cantidad_destino': cantidad_destino,}
    return JsonResponse(data)


def delete_equiv(request):
    id_equiv = request.GET.get('id_equiv', None)
    equiv = Equivalencias.objects.get(id=id_equiv)
    equiv.activo = False
    equiv.save()
    data = { 'success': True,}
    return JsonResponse(data)

def check_equiv_destino(request):
    id_product = request.GET.get('id_product', None)
    id_unidad_origen = request.GET.get('id_unidad_origen', None)
    product = Product.objects.get(id=id_product)

    uni = UnidadDeMedida.objects.get(id=id_unidad_origen)
    equivs = Equivalencias.objects.filter(id_product=product, id_unidad_origen=id_unidad_origen, activo = True)
    unidadesTotal = UnidadDeMedida.objects.all()

    data = {
        'id_product': id_product,
        'unidadesTotal': [],
        'unidades': [],
    }
    for uni in unidadesTotal:
        data['unidadesTotal'].append(uni.id)
    for equi in equivs:
        data['unidades'].append(equi.id_unidad_destino.id)
    print(data)
    return JsonResponse(data)






#
