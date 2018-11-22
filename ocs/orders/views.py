"""
created by:     Django
description:    This are the views of the providers that helps their tasks
                to accomplish
modify by:      Fatima
modify date:    12/11/18
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, F
from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required


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

from inventory.models import LinkedInventory
from inventory.models import LinkedProductRecord


from django.http import JsonResponse
import json


def make_order(request):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)
    my_providers = LinkWithF.objects.filter(id_franchise = franchise, active = True)
    data ={
        'usuario': u,
        #'franchise': franchise,
        'my_providers': my_providers,
    }
    return render(request, 'orders/make_order.html', data)

def make_order_to(request, id_provider):
    #sacamos el usuario, su franquicia y sus proveedores
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)
    my_providers = LinkWithF.objects.filter(id_franchise = franchise, active = True)
    #de sus proveedores sacamos al que se le hará el pedido y sus productos con precio activos
    provider = Provider.objects.get(id= id_provider)
    products = Product.objects.filter(id_provider=provider, activo=True)
    complete_products = CompleteProduct.objects.filter(id_product__in=products, activo=True)
    id_product_aux = []
    for comp in complete_products:
        id_product_aux.append(comp.id_product.id)
    my_products = Product.objects.filter(id__in = id_product_aux).order_by('nombre')
    #creamos la estructura a regresar (OUTPUT)
    data = {
        'usuario': u,
        'my_providers': my_providers,
        'provider':provider,
        'products':my_products,
        'order_to_edit': False,
        'orders': None,
        'orders_products': None,
        'orders_day': None,
        'orders_status': None,
    }
    exists = Order.objects.filter(id_franchise=franchise, id_provider=provider, activo=True).exists()
    if exists:
        data['order_to_edit'] = True
        orders = Order.objects.filter(id_franchise=franchise, id_provider=provider, activo=True)
        exists = OrderInStatus.objects.filter(id_pedido__in = orders, id_status__in=[1,2,3], activo = True).exists()
        if exists:
            order_s = OrderInStatus.objects.get(id_pedido__in = orders, id_status__in=[1,2,3], activo = True)
            prods = OrderProductInStatus.objects.filter(id_pedido=order_s.id_pedido, activo=True)
            for p in prods:
                products = products.exclude(id=p.id_complete_product.id_product.id)

            data['orders'] = order_s.id_pedido
            data['orders_products'] = prods
            data['products'] = products
            #aux_date = str(ord.id_pedido.fecha_pedido.year)+'-'+str(ord.id_pedido.fecha_pedido.month)+'-'+str(ord.id_pedido.fecha_pedido.day)
            #data['orders_date'] = (aux_date)
            aux_day = order_s.id_pedido.fecha_ideal.weekday()
            if aux_day == 0: day = 'LUNES'
            elif aux_day == 1: day = 'MARTES'
            elif aux_day == 2: day = 'MIÉRCOLES'
            elif aux_day == 3: day = 'JUEVES'
            elif aux_day == 4: day = 'VIERNES'
            elif aux_day == 5: day = 'SÁBADO'
            elif aux_day == 6: day = 'DOMINGO'
            data['orders_day'] = day
            data['orders_status'] = order_s
        else:
            data['order_to_edit'] = False
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

    without_equiv = CompleteProduct.objects.filter(id_product=product, id_unidad=unidad, activo=True).exists()
    if without_equiv:
        complete_product = CompleteProduct.objects.get(id_product=product, id_unidad=unidad, activo=True)
    else:
        equiv = Equivalencias.objects.filter(id_product = product, id_unidad_destino = unidad, activo = True)[0]
        complete_product = CompleteProduct.objects.get(id_product=product, id_unidad=equiv.id_unidad_origen, activo=True)

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
    alrready_in_order = OrderProductInStatus.objects.filter(id_pedido=order, id_complete_product=complete_product, activo=True).exists()
    if alrready_in_order:
        order_product = OrderProductInStatus.objects.get(id_pedido=order,id_complete_product=complete_product, activo=True)
        order.precio_total = order.precio_total-order_product.total
        order.cantidad_productos = order.cantidad_productos-1
        order.save()
        order_product.cantidad = Decimal(cantidad_pedida)
        if without_equiv:
            order_product.precio_por_unidad = complete_product.id_price.cantidad
            order_product.total = order_product.cantidad*order_product.precio_por_unidad
        else:
            precio_por_equiv = complete_product.id_price.cantidad*((equiv.cantidad_origen/equiv.cantidad_destino))
            order_product.precio_por_unidad = precio_por_equiv
            order_product.total = order_product.cantidad*order_product.precio_por_unidad
        order_product.id_unidad = unidad
    else:
        if without_equiv:
            order_product = OrderProductInStatus(id_pedido=order,
                                                    id_complete_product=complete_product,
                                                    id_unidad = unidad,
                                                    cantidad = Decimal(cantidad_pedida),
                                                    precio_por_unidad = complete_product.id_price.cantidad,
                                                    total = Decimal(cantidad_pedida)*complete_product.id_price.cantidad,
                                                    fecha=timezone.now(),
                                                    activo=True)
        else:
            precio_por_equiv = complete_product.id_price.cantidad*((equiv.cantidad_origen/equiv.cantidad_destino))
            order_product = OrderProductInStatus(id_pedido=order,
                                                    id_complete_product=complete_product,
                                                    id_unidad = unidad,
                                                    cantidad = Decimal(cantidad_pedida),
                                                    precio_por_unidad = precio_por_equiv,
                                                    total = Decimal(cantidad_pedida)*precio_por_equiv,
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
                'cantidad': order_product.cantidad,
                'ud_medida': unidad.abreviacion,
                'id_product': product.id,
                'producto': product.nombre.capitalize(),
                'precio': order_product.precio_por_unidad,
                'total': order_product.total,
                'precio_total': order.precio_total,
                'cantidad_total': order.cantidad_productos,}
    return JsonResponse(data)

def delete_product_from_order(request):
    id_pedido = request.GET.get('id_pedido', None)
    id_prod_ord = request.GET.get('id_prod_ord', None)

    pedido = Order.objects.get(id=id_pedido)
    order_product = OrderProductInStatus.objects.get(id=id_prod_ord)

    pedido.cantidad_productos = pedido.cantidad_productos-1
    pedido.precio_total = pedido.precio_total-order_product.total
    pedido.save()
    complete_product = order_product.id_complete_product
    order_product.delete()
    product = complete_product.id_product
    data = { 'success':True,
                'id_product':product.id,
                'nombre_product':product.nombre.capitalize(),
                'cantidad_total':pedido.cantidad_productos,
                'precio_total':pedido.precio_total,}
    return JsonResponse(data)

# Function that let the providers to edit its company info
@login_required
def order_detail (request, id_order):
    u = OCSUser.objects.get(user = request.user)
    order = Order.objects.get(id = id_order)
    products_list = OrderProductInStatus.objects.filter(id_pedido = order, activo = True)
    #Para cambiar el estado de la orden
    order_s = OrderInStatus.objects.get(id_pedido=order, activo=True)
    pedido = OrderStatus.objects.get(id = 2)
    if(order_s.id_status == pedido):
        status = OrderStatus.objects.get(id = 3)
        order_s.id_status = status
        order_s.save()
    data = {
        'usuario': u,
        'data':order,
        'products_list':products_list,
    }
    return render(request, 'orders/order_detail.html', data)

@login_required
def consult_orders (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    prov = ocs_user.id_provider_id
    user = request.user
    provider = Group.objects.get(name = "Administrador de empresa")

    #filtro para aislar a la columna id, sirve para solo seleccionar las ordenes de tal proveedor
    orders = Order.objects.filter(id_provider=prov, activo=True)
    pedido = OrderInStatus.objects.filter(id_pedido__in = orders, id_status = 2, activo = 1)
    recibido = OrderInStatus.objects.filter(id_pedido__in = orders, id_status = 3, activo = 1)
    preparar = OrderInStatus.objects.filter(id_pedido__in = orders, id_status = 6, activo = 1)
    incompletos = OrderInStatus.objects.filter(id_pedido__in = orders, id_status = 7, activo = 1)

    if len(pedido) != 0 or len(recibido) != 0:empty_list = 0
    else:empty_list = 1

    if len(preparar) == 0:empty_list_re = 1
    else:empty_list_re = 0

    if len(incompletos) == 0:
        empty_list_in = 1
    else:
        empty_list_in = 0

    data = {
        'usuario':ocs_user,
        'empty_list':empty_list,
        'empty_list_re':empty_list_re,
        'empty_list_in':empty_list_in,
        'pedido':pedido,
        'recibido':recibido,
        'preparar':preparar,
        'incompletos':incompletos,
    }
    return render(request, 'orders/consult_orders.html', data)

def order_detail (request, id_order):
    exist = Order.objects.filter(id = id_order).exists()
    if exist == False:
        return redirect('/')
    else:
        order = Order.objects.get(id = id_order)
    u = OCSUser.objects.get(user = request.user)
    aux = False
    if u.id_provider is None:
        franchise = Franchise.objects.get(id = u.id_franchise.id)
        if order.id_franchise == franchise:
            aux = True
            other = 'franchise/home.html'
    else:
        provider = Provider.objects.get(id = u.id_provider.id)
        if order.id_provider == provider:
            aux = True
            other = 'provider/home.html'
    if aux:
        products_list = OrderProductInStatus.objects.filter(id_pedido = order, activo = True)
        #Para cambiar el estado de la orden
        order_s = OrderInStatus.objects.get(id_pedido=order, activo=True)
        pedido = OrderStatus.objects.get(id = 2)
        if(order_s.id_status == pedido):
            status = OrderStatus.objects.get(id = 3)
            order_s.id_status = status
            order_s.save()
        data = {
            'usuario': u,
            'order_s':order_s,
            'data':order,
            'aux':other,
            'products_list':products_list,
        }
        return render(request, 'orders/order_detail.html', data)
    else:
        return redirect('/')
        empty_list_re = 0

    if (provider in user.groups.all()): #Checks privileges of owner
        return render(request, 'orders/consult_orders.html', {'usuario':ocs_user, 'edit':True, 'empty_list':empty_list, 'pedido':pedido, 'recibido':recibido, 'preparar':preparar, 'empty_list_re':empty_list_re})
    else:
        return redirect('../../')


def cancel_order(request):
    id_pedido = request.GET.get('id_pedido', None)
    id_provider = request.GET.get('id_provider', None)

    order = Order.objects.get(id = id_pedido, activo=True)
    order.activo = False
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)
    order_status = OrderStatus.objects.get(id=5)
    new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
    new_order_in_status.save()
    order_in_status.activo = False
    order_in_status.save()
    order.save()
    data = { 'success': True, }
    return JsonResponse(data)

def send_order(request):
    id_pedido = request.GET.get('id_pedido', None)
    id_provider = request.GET.get('id_provider', None)

    order = Order.objects.get(id = id_pedido, activo=True)
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)
    order_status = OrderStatus.objects.get(id=2)
    new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
    new_order_in_status.save()
    order_in_status.activo = False
    order_in_status.save()
    data = { 'success': True, }
    return JsonResponse(data)

def bloquear_pedido(request):
    id_pedido = request.GET.get('id_pedido', None)
    order = Order.objects.get(id = id_pedido, activo=True)
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)
    order_status = OrderStatus.objects.get(id=6)
    if order_in_status.id_status != order_status:
        new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
        new_order_in_status.save()
        order_in_status.activo = False
        order_in_status.save()
    data = { 'success': True, }
    return JsonResponse(data)

def desbloquear_pedido(request):
    id_pedido = request.GET.get('id_pedido', None)
    order = Order.objects.get(id = id_pedido, activo=True)
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)
    order_status = OrderStatus.objects.get(id=3)
    if order_in_status.id_status != order_status:
        new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
        new_order_in_status.save()
        order_in_status.activo = False
        order_in_status.save()
    data = { 'success': True, }
    return JsonResponse(data)

def rechazar_pedido(request):
    id_pedido = request.GET.get('id_pedido', None)

    order = Order.objects.get(id = id_pedido, activo=True)
    order.activo = False
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)
    order_status = OrderStatus.objects.get(id=4)
    new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
    new_order_in_status.save()
    order_in_status.activo = False
    order_in_status.save()
    order.save()
    data = { 'success': True, }
    return JsonResponse(data)


def consult_order_history_prov(request):
    ocs_user = OCSUser.objects.get(user = request.user)
    prov = ocs_user.id_provider
    #filtro para aislar a la columna id, sirve para solo seleccionar las ordenes de tal proveedor
    orders = Order.objects.filter(id_provider=prov, activo=False)
    status = OrderInStatus.objects.filter(id_pedido__in = orders, activo=True)
    data = {
        'usuario':ocs_user,
        'provider':prov,
        'aux':'provider/home.html',
        'orders':status,
    }
    return render(request, 'orders/consult_orders_history.html', data)

def consult_order_history_franq(request):
    ocs_user = OCSUser.objects.get(user = request.user)
    sucu = ocs_user.id_franchise
    #filtro para aislar a la columna id, sirve para solo seleccionar las ordenes de tal proveedor
    orders = Order.objects.filter(id_franchise=sucu, activo=False)
    status = OrderInStatus.objects.filter(id_pedido__in = orders, activo=True)

    ordersaux = Order.objects.filter(id_franchise=sucu, activo=True)
    statusaux = OrderInStatus.objects.filter(id_pedido__in = ordersaux, id_status__in=[6,7], activo=True)

    data = {
        'usuario':ocs_user,
        'franchise':sucu,
        'aux':'franchise/home.html',
        'orders':status,
        'pending':statusaux,
    }
    return render(request, 'orders/consult_orders_history.html', data)

def register_arrival (request, id_order):
    exist = Order.objects.filter(id = id_order).exists()
    if exist == False:
        return redirect('/')
    else:
        order = Order.objects.get(id = id_order)
    u = OCSUser.objects.get(user = request.user)
    aux = False
    if u.id_provider is None:
        franchise = Franchise.objects.get(id = u.id_franchise.id)
        if order.id_franchise == franchise:
            products_list = OrderProductInStatus.objects.filter(id_pedido = order, activo = True)
            #Para cambiar el estado de la orden
            order_s = OrderInStatus.objects.get(id_pedido=order, activo=True)
            pedido = OrderStatus.objects.get(id = 2)
            if(order_s.id_status == pedido):
                status = OrderStatus.objects.get(id = 3)
                order_s.id_status = status
                order_s.save()
            data = {
                'usuario': u,
                'order_s':order_s,
                'data':order,
                'products_list':products_list,
            }
            return render(request, 'orders/register_arrival.html', data)
        else:
            return redirect('/')
    else:
        return redirect('/')

def complete_order(request):
    id_pedido = request.GET.get('id_pedido', None)
    print(id_pedido)
    order = Order.objects.get(id = id_pedido, activo=True)
    order_in_status = OrderInStatus.objects.get(id_pedido=order, activo=True)

    order_status = OrderStatus.objects.get(id=8)
    new_order_in_status = OrderInStatus(id_pedido=order,id_status=order_status,fecha=timezone.now(), activo=True)
    new_order_in_status.save()

    order_in_status.activo = False
    order_in_status.save()

    order.activo = False
    order.save()

    productos = OrderProductInStatus.objects.filter(id_pedido = order, activo=True)
    for p in productos:
        exist = LinkedInventory.objects.filter(id_franchise=order.id_franchise, id_product=p.id_complete_product.id_product).exists()
        if exist:
            prod_inv = LinkedInventory.objects.get(id_franchise=order.id_franchise, id_product=p.id_complete_product.id_product)
            if p.id_unidad == prod_inv.id_unidad:
                prod_inv.amount = prod_inv.amount + p.cantidad
            else:
                exist = Equivalencias.objects.filter(id_product = p.id_complete_product.id_product, id_unidad_origen = prod_inv.id_unidad).exists()
                if exist:
                    equiv = Equivalencias.objects.get(id_product = p.id_complete_product.id_product, id_unidad_origen = prod_inv.id_unidad)
                    cant_por_equiv = (p.cantidad*equiv.cantidad_origen)/equiv.cantidad_destino
                    prod_inv.amount = prod_inv.amount + cant_por_equiv
                else:
                    equiv = Equivalencias.objects.get(id_product = p.id_complete_product.id_product, id_unidad_destino = prod_inv.id_unidad)
                    cant_por_equiv = (p.cantidad*equiv.cantidad_destino)/equiv.cantidad_origen
                    prod_inv.amount = prod_inv.amount + cant_por_equiv
        else:
            prod_inv = LinkedInventory(id_franchise=order.id_franchise, id_product=p.id_complete_product.id_product, id_unidad=p.id_unidad, amount = p.cantidad)
        prod_inv.save()
        bitacora = LinkedProductRecord(id_franchise=order.id_franchise,id_linked_product = prod_inv,id_unidad=p.id_unidad,date = timezone.now(),comment = "Ingreso del pedido #"+str(order.id),amount = p.cantidad,io = True)
        bitacora.save()
    data = { 'success': True, }
    return JsonResponse(data)
















def has_permission(ocs_u, is_provider, id_company, id_rol):
    u = OCSUser.objects.get(id = ocs_u)
    user = User.objects.get(id = u.user)
    user_groups = user.groups.all()
    if u.id_provider is None:
        if is_provider:
            return False
        fran = Franchise.objects.get(id = u.id_franchise)
        if fran.id == id_company:
            for g in user_groups:
                if id_rol == g.id:
                    return True
        return False
    elif u.id_franchise is None:
        if is_provider:
            prov = Provider.objects.get(id = u.id_provider)
            if prov.id == id_company:
                for g in user_groups:
                    if id_rol == g.id:
                        return True
        return False
    else: return False


#
