"""
Created by : Django
Description: Views file for the Inventory module
Modified by: Dante F
Modify date: 1-11-18
"""
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import OCSUser
from .models import PrivateProduct, PrivateProductRecord
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
import xlwt
from django.contrib.auth.models import User
import datetime


# Create your views here.
@login_required
def show_inventory(request):
    """
    By: DanteMaxF
    Function used to display a table of the private products of a franchise
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Query set of the inventory
    """
    u = OCSUser.objects.get(user = request.user)
    product_list = PrivateProduct.objects.filter(id_franchise=u.id_franchise)


    return render(request, 'inventory/show_inventory.html', {
            'usuario' : u,
            'product_list' : product_list,
            })

@login_required
def register_private_product(request):
    """
    By: DanteMaxF
    Function used to register the new product a franchise wants to register
    INPUT
        - Request method with the values of the session
        - Context variables throug a post of the new product
    OUTPUT
        - Redirect to the inventory table
        - Update of the inventory database
    """
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        p_name = request.POST['product_name']
        p_desc = request.POST['product_desc']
        p_amount = int(request.POST['product_amount'])
        p_unit = request.POST['product_unit']

        if (p_name=='' or p_desc=='' or p_amount=='' or p_unit==''):
            messages.warning(request, 'ERROR: Por favor llena todos los campos')
            return redirect(reverse('franchise:inventory:show_inventory'))

        if (p_amount < 0):
            messages.warning(request, 'ERROR: No puedes ingresar números menores a cero')
            return redirect(reverse('franchise:inventory:show_inventory'))

        # Check if product name already exist
        new_product = PrivateProduct(id_franchise=u.id_franchise, name=p_name, description=p_desc, amount=p_amount, unit=p_unit)
        try:
            product_test = PrivateProduct.objects.get(name=p_name, id_franchise=u.id_franchise)
        except:
            new_product.save()
            newRecord = PrivateProductRecord(id_franchise=u.id_franchise, id_private_product=new_product, date=datetime.datetime.now(), comment="NUEVO PRODUCTO REGISTRADO POR: "+u.user.first_name+" "+u.user.last_name, amount=int(p_amount), io=True)
            newRecord.save()
            messages.success(request, 'Producto registrado!')
        else:
            messages.warning(request, 'ERROR: Ya existe un producto con este nombre')
            return redirect(reverse('franchise:inventory:show_inventory'))
    return redirect(reverse('franchise:inventory:show_inventory'))

@login_required
def create_excel(request):
    """
    By: DanteMaxF
    Function used to generate a excel document
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Redirect to the inventory table
        - An  excel document to be downloaded
    """
    today = datetime.date.today()
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        product_list = PrivateProduct.objects.filter(id_franchise=u.id_franchise)
        # Generate XLS
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="'+u.id_franchise.nombre+'"_inventario.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Inventory')

        # Sheet header, first row
        row_num = 3

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        ws.write_merge(0, 0, 0, 4, u.id_franchise.nombre, font_style)
        ws.write_merge(1, 1, 0, 4, 'Inventario de Productos', font_style)
        ws.write_merge(2, 2, 0, 4, ''+str(today.strftime('%d-%m-%Y')), font_style)

        columns = ['Producto', 'Descripción', 'Cantidad', 'Unidad']

        ws.write(row_num, 0, '#', font_style)

        for col_num in range(len(columns)):
            ws.write(row_num, col_num+1, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = PrivateProduct.objects.filter(id_franchise=u.id_franchise)
        counter = 1
        for row in rows:
            row_num += 1
            ws.write(row_num, 0, str(counter), font_style)
            ws.write(row_num, 1, row.name, font_style)
            ws.write(row_num, 2, row.description, font_style)
            ws.write(row_num, 3, row.amount, font_style)
            ws.write(row_num, 4, row.unit, font_style)
            counter = counter +1

        wb.save(response)
        return response
    return redirect(reverse('franchise:inventory:show_inventory'))

@login_required
def update_private_product(request):
    """
    By: DanteMaxF
    Function used to update the inputs and outputs of the
    private products in the inventory
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Redirect to the inventory table
        - The updated database of the inventory
    """
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        p_id = request.POST['id_product']
        p_io = request.POST['product_io']
        p_amount = request.POST['product_amount']
        p_comment = request.POST['product_comment']

        if (p_id=='' or p_io=='' or p_amount=='' or p_comment==''):
            messages.warning(request, 'ERROR: Por favor llena todos los campos.')
            return redirect(reverse('franchise:inventory:show_inventory'))

        if (int(p_amount) < 1):
            messages.warning(request, 'ERROR: No se pueden insertar cantidades menores a 1.')
            return redirect(reverse('franchise:inventory:show_inventory'))

        try:
            updated_product = PrivateProduct.objects.get(id=p_id)
        except:
            messages.warning(request, 'ERROR: El producto que quieres actualizar no existe')
        else:
            if (p_io == 'in'):
                updated_product.amount = updated_product.amount + int(p_amount)
                updated_product.save()
                newRecord = PrivateProductRecord(id_franchise=u.id_franchise, id_private_product=updated_product, date=datetime.datetime.now(), comment=p_comment, amount=int(p_amount), io=True)
                newRecord.save()
                messages.success(request, 'EXITO: Se ha registrado una ENTRADA del producto:   '+updated_product.name)
            elif (p_io == 'out'):
                if (int(p_amount) > updated_product.amount):
                    messages.warning(request, 'ERROR: Estás intentando retirar una cantidad mayor a la que tienes!')
                else:
                    updated_product.amount = updated_product.amount-int(p_amount)
                    updated_product.save()
                    newRecord = PrivateProductRecord(id_franchise=u.id_franchise, id_private_product=updated_product, date=datetime.datetime.now(), comment=p_comment, amount=int(p_amount), io=False)
                    newRecord.save()
                    messages.success(request, 'EXITO: Se ha registrado una SALIDA del producto:   '+updated_product.name)
            else:
                messages.warning(request, 'ERROR')

    return redirect(reverse('franchise:inventory:show_inventory'))

@login_required
def show_inventory_records(request):
    """
    By: DanteMaxF
    Function used to display a record table of the different inputs/outputs on the
    inventory
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Query set of the inventory records
    """
    u = OCSUser.objects.get(user = request.user)
    record_list = PrivateProductRecord.objects.filter(id_franchise=u.id_franchise)
    return render(request, 'inventory/show_records.html', {
            'usuario' : u,
            'record_list': record_list
            })
