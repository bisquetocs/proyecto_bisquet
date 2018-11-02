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
from .models import PrivateProduct
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic

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

        if (p_name=='' or p_desc=='' or p_amount==''):
            messages.warning(request, 'ERROR: Por favor llena todos los campos')
            return redirect(reverse('franchise:inventory:show_inventory'))

        if (p_amount < 0):
            messages.warning(request, 'ERROR: No puedes ingresar números menores a cero')
            return redirect(reverse('franchise:inventory:show_inventory'))

        # Check if product name already exist
        new_product = PrivateProduct(id_franchise=u.id_franchise, name=p_name, description=p_desc, amount=p_amount)
        try:
            product_test = PrivateProduct.objects.get(name=p_name)
        except:
            new_product.save()
            messages.success(request, 'Producto registrado!')
        else:
            messages.warning(request, 'ERROR: Ya existe un producto con este nombre')
            return redirect(reverse('franchise:inventory:show_inventory'))
    return redirect(reverse('franchise:inventory:show_inventory'))

@login_required
def create_pdf(request):
    """
    By: DanteMaxF
    Function used to generate a PDF document
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Redirect to the inventory table
        - A  PDF document to be downloaded
    """
    u = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        product_list = PrivateProduct.objects.filter(id_franchise=u.id_franchise)
        return HttpResponse('CREATE PDF')
    return redirect(reverse('franchise:inventory:show_inventory'))
