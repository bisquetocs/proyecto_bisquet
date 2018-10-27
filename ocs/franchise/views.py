"""
Description: Views file for the Franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterFranchiseForm
from provider.models import LinkWithF, Provider
from accounts.models import OCSUser

from .models import Franchise, PrivateProduct

@login_required
def registerFranchise(request):
    if request.method == 'POST':
        register_form = RegisterFranchiseForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            return redirect('../franchise/home')
    else:
        u = OCSUser.objects.get(user = request.user)
        if u.id_franchise!=None:
            return redirect('../franchise/home')
        elif u.id_franchise==None and (u.id_provider!=None):
            return redirect('../provider/home')
        else:
            register_form = RegisterFranchiseForm()
            return render(request, 'franchise/register.html', {'register_form': register_form})

@login_required
def home(request):
    u = OCSUser.objects.get(user = request.user)
    if u.id_franchise!=None:
        return render(request, 'franchise/home.html', {'usuario':u,})
    else:
        return redirect('../')

@login_required
def link_provider(request):
    """
     Function used to link a franchise with a provider using a link code
     INPUT
        - Request method with the values of the session
        - A post method with the link code inserted by the user
     OUTPUT
        - A reload of the same page and a response of the status of the process
    """
    u = OCSUser.objects.get(user = request.user)
    code = ''
    f_name = ''
    if request.method == 'POST':
        code = request.POST['link_code']
        try:
            l = LinkWithF.objects.get(link_code=code)
            if l.used:
                messages.warning(request, 'El código ya fue utilizado, por favor, solicita a tu proveedor que te genere un código nuevo.')
            else:
                l.id_franchise = u.id_franchise
                l.active = True
                l.used = True
                l.save()
                f_name = l.id_provider.nombre
                messages.success(request, '¡EXITO! Te has relacionado con '+f_name)
        except:
            messages.error(request, 'El código no coincide con ninguno registrado, ingrésalo de nuevo o consulta a tu proveedor..')
    return render(request, 'link_provider/link_with_provider.html', {
            'usuario' : u,
            'code' : code,
            'franchise_name' : f_name
            })

@login_required
def my_providers(request):
    """
     Function used to display the providers linked with the user using the system
     INPUT
        - Request method with the values of the session
     OUTPUT
        - Query set with the list of providers
    """
    empty_list = 0
    u = OCSUser.objects.get(user = request.user)
    relation_list = LinkWithF.objects.filter(id_franchise=u.id_franchise)
    if len(relation_list) == 0:
        empty_list = 1

    return render(request, 'my_providers/consult_providers.html', {
            'usuario' : u,
            'relation_list' : relation_list,
            'empty_list' : empty_list
            })


@login_required
def provider_detail(request, id_provider):
    """
     Function that displays the details of the provider selected in the provider table
     INPUT
        - Request method with the values of the session
        - Id of the provider to consult_providers
     OUTPUT
        - Detailed information of each attribute from the provider
    """
    success = True
    u = OCSUser.objects.get(user = request.user)
    p = Provider()
    relation_list = LinkWithF.objects.filter(id_franchise=u.id_franchise, id_provider=id_provider)
    try:
        p = Provider.objects.get(id=id_provider)
        if len(relation_list) == 0:
            success = False
    except:
        success = False
        raise Http404("Provider does not exist")
    return render(request, 'my_providers/provider_detail.html', {
            'usuario' : u,
            'success' : success,
            'provider' : p,
            })


@login_required
def show_inventory(request):
    """
    Function used to display a table of the private products od a franchise
    INPUT
        - Request method with the values of the session
    OUTPUT
        - Query set of the inventory
    """
    empty_field = 0
    amount_error = 0
    product_already_exists = 0
    registration_success = 0

    u = OCSUser.objects.get(user = request.user)
    product_list = PrivateProduct.objects.filter(id_franchise=u.id_franchise)


    if request.method == 'POST':
        p_name = request.POST['product_name']
        p_desc = request.POST['product_desc']
        p_amount = int(request.POST['product_amount'])

        if (p_name=='' or p_desc=='' or p_amount==''):
            empty_field = 1
            return render(request, 'inventory/show_inventory.html', {
                    'usuario' : u,
                    'product_list' : product_list,
                    'empty_field' : empty_field,
                    'amount_error' : amount_error,
                    'product_already_exists' : product_already_exists,
                    'registration_success' : registration_success
                    })
        if (p_amount < 0):
            amount_error = 1
            return render(request, 'inventory/show_inventory.html', {
                    'usuario' : u,
                    'product_list' : product_list,
                    'empty_field' : empty_field,
                    'amount_error' : amount_error,
                    'product_already_exists' : product_already_exists,
                    'registration_success' : registration_success
                    })
        # Check if product name already exist
        new_product = PrivateProduct(id_franchise=u.id_franchise, name=p_name, description=p_desc, amount=p_amount)
        try:
            product_test = PrivateProduct.objects.get(name=p_name)
        except:
            new_product.save()
            registration_success = 1
        else:
            product_already_exists = 1


    return render(request, 'inventory/show_inventory.html', {
            'usuario' : u,
            'product_list' : product_list,
            'empty_field' : empty_field,
            'amount_error' : amount_error,
            'product_already_exists' : product_already_exists,
            'registration_success' : registration_success
            })


@login_required
def profile (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    return render(request, 'franchise/profile.html', {'usuario':ocs_user,})

@login_required
def edit_franchise (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        f = Franchise.objects.get(id=ocs_user.id_franchise.id)
        f.nombre=request.POST['nombre']
        f.razon_social=request.POST['razon_social']
        f.rfc=request.POST['rfc']
        f.domicilio=request.POST['domicilio']
        f.save()
        messages.success(request, 'La información se actualizó con éxito!')
        return redirect(reverse('franchise:profile'))
    else:
        return render(request, 'franchise/profile.html', {'usuario':ocs_user, 'edit':True,})










#
