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
from provider.models import LinkWithF
from franchise.models import Franchise
from products.models import Product

from .models import Order
from .models import OrderProductStatus
from .models import OrderProductInStatus
from .models import OrderStatus
from .models import OrderInStatus

from products.models import UnidadDeMedida
from products.models import Price
from products.models import CompleteProduct
from products.models import Equivalencias



from django.http import JsonResponse
import json


def make_order(request):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)
    my_providers = LinkWithF.objects.filter(id_franchise = franchise, active = True)
    data ={
        'usuario': u,
        'franchise': franchise,
        'my_providers': my_providers,
    }
    return render(request, 'orders/make_order.html', data)

def make_order_to(request, id_provider):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)
    my_providers = LinkWithF.objects.filter(id_franchise = franchise, active = True)
    provider = Provider.objects.get(id= id_provider)
    products = Product.objects.filter(id_provider=provider, activo=True).order_by('nombre')
    #unidad_price = CompleteProduct.objects.filter(id_product__in = prodcts, activo=True)
    data = {
        'usuario': u,
        'franchise': franchise,
        'my_providers': my_providers,
        'provider':provider,
        'products':products,
        'order_to_edit': False,
        'too_late': False,
        'just_one': False,
        'orders': None,
        'orders_products': None,
        'orders_id': [],
        'orders_date': [],
        'orders_day': [],
        'orders_status': [],
        'orders_status_desc': []
    }
    exists = Order.objects.filter(id_franchise=franchise, id_provider=provider, activo=True, arrive=False).exists()
    if exists:
        orders = Order.objects.filter(id_franchise=franchise, id_provider=provider, activo=True, arrive=False)
        exists = OrderInStatus.objects.filter(id_pedido__in = orders, activo = True).exists()
        if exists:
            my_order_status = OrderInStatus.objects.filter(id_pedido__in = orders, activo = True)
            data['order_to_edit'] = True
            if my_order_status.count() == 1:
                data['just_one'] = True
                ord = OrderInStatus.objects.get(id_pedido__in = orders, activo = True)
                prods = OrderProductInStatus.objects.filter(id_pedido=ord.id_pedido, activo=True)
                for p in prods:
                    print(p.id_complete_product.id_product.id)##########
                    products = products.exclude(id=p.id_complete_product.id_product.id)

                if ord.id_status.id==1 or ord.id_status.id==2 or ord.id_status.id==3:
                    data['orders'] = ord.id_pedido
                    data['orders_products'] = prods
                    data['products'] = products
                    data['orders_id'] = (ord.id_pedido.id)
                    aux_date = str(ord.id_pedido.fecha_pedido.year)+'-'+str(ord.id_pedido.fecha_pedido.month)+'-'+str(ord.id_pedido.fecha_pedido.day)
                    data['orders_date'] = (aux_date)
                    aux_day = ord.id_pedido.fecha_pedido.weekday()
                    if aux_day == 0: day = 'LUNES'
                    elif aux_day == 1: day = 'MARTES'
                    elif aux_day == 2: day = 'MIÉRCOLES'
                    elif aux_day == 3: day = 'JUEVES'
                    elif aux_day == 4: day = 'VIERNES'
                    elif aux_day == 5: day = 'SÁBADO'
                    elif aux_day == 6: day = 'DOMINGO'
                    data['orders_day'] = day
                    data['orders_status'] = (ord.id_status.nombre)
                    data['orders_status_desc'] = (ord.id_status.descripcion)
                else:
                    data['too_late'] = True
            else:
                for ord in my_order_status:
                    # Aqui están los id de los estados (Guardado, Pedido, Aceptado)
                    if ord.id_status.id==1 or ord.id_status.id==2 or ord.id_status.id==3:
                        data['orders'].append(ord)
                        data['orders_id'].append(ord.id_pedido.id)
                        aux_date = str(ord.id_pedido.fecha_pedido.year)+'-'+str(ord.id_pedido.fecha_pedido.month)+'-'+str(ord.id_pedido.fecha_pedido.day)
                        data['orders_date'].append(aux_date)
                        aux_day = ord.id_pedido.fecha_pedido.weekday()
                        if aux_day == 0: day = 'LUNES'
                        elif aux_day == 1: day = 'MARTES'
                        elif aux_day == 2: day = 'MIÉRCOLES'
                        elif aux_day == 3: day = 'JUEVES'
                        elif aux_day == 4: day = 'VIERNES'
                        elif aux_day == 5: day = 'SÁBADO'
                        elif aux_day == 6: day = 'DOMINGO'
                        data['orders_day'].append(day)
                        data['orders_status'].append(ord.id_status.nombre)
                        data['orders_status_desc'].append(ord.id_status.descripcion)
                    else:
                        data['too_late'] = True

    return render(request, 'orders/make_order_to.html', data)

def add_product_to_order(request):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)

    id_pedido = request.GET.get('id_pedido', None)
    id_provider = request.GET.get('id_provider', None)
    nombre_product = request.GET.get('nombre_producto', None)
    ud_medida = request.GET.get('ud_medida', None)
    cantidad_pedida = request.GET.get('cantidad_pedida', None)

    provider = Provider.objects.get(id=id_provider)
    product = Product.objects.get(nombre=nombre_product,id_provider=provider)
    unidad = UnidadDeMedida.objects.get(id=ud_medida)
    complete_product = CompleteProduct.objects.get(id_product=product, id_unidad=unidad, activo=True)

    if id_pedido is None or id_pedido == '':
        order = Order(id_franchise=franchise,
                        id_provider=provider,
                        fecha_pedido=timezone.now(),
                        fecha_ideal=request.GET.get('date', None),
                        cantidad_productos=0,
                        precio_total=None,
                        activo=True,
                        arrive=False)
        order.save()
        order_status = OrderInStatus(id_pedido=order,
                                        id_status=OrderStatus.objects.get(id=1),
                                        fecha=timezone.now(),
                                        activo=True)
        order_status.save()
    else:
        order = Order.objects.get(id=id_pedido)
    aux = int(cantidad_pedida)*complete_product.id_price.cantidad
    order_product = OrderProductInStatus(id_pedido=order,
                                            id_complete_product=complete_product,
                                            cantidad=cantidad_pedida,
                                            total = aux,
                                            fecha=timezone.now(),
                                            activo=True)
    order_product.save()
    if order.precio_total is None:
        order.precio_total = order_product.total
    else:
        order.precio_total = order.precio_total+order_product.total
    order.cantidad_productos = order.cantidad_productos+1
    order.save()
    data = { 'success': True,
                'id_pedido':order.id,
                'id_ord_prod':order_product.id,
                'cantidad': cantidad_pedida,
                'ud_medida': unidad.abreviacion,
                'id_product': product.id,
                'producto': nombre_product,
                'precio': order_product.id_complete_product.id_price.cantidad,
                'total': order_product.total,
                'precio_total': order.precio_total,
                'cantidad_total': order.cantidad_productos,}
    return JsonResponse(data)

def delete_product_from_order(request):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)

    id_pedido = request.GET.get('id_pedido', None)
    id_provider = request.GET.get('id_provider', None)
    id_prod_ord = request.GET.get('id_prod_ord', None)

    pedido = Order.objects.get(id=id_pedido)
    provider = Provider.objects.get(id=id_provider)
    order_product = OrderProductInStatus.objects.get(id=id_prod_ord)

    pedido.cantidad_productos = pedido.cantidad_productos-1
    pedido.precio_total = pedido.precio_total-order_product.total
    pedido.save()
    order_product.activo = False
    order_product.save()
    complete_product = order_product.id_complete_product
    product = complete_product.id_product
    data = { 'success':True,
                'id_product':product.id,
                'nombre_product':product.nombre.capitalize(),}
    return JsonResponse(data)











#
