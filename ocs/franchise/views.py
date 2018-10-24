from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
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
            return render(request, 'franchise/home.html')
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
    success = ''
    u = OCSUser.objects.get(user = request.user)
    code = ''
    f_name = ''
    if request.method == 'POST':
        code = request.POST['link_code']
        try:
            l = LinkWithF.objects.get(link_code=code)
            if l.used:
                success = 2
            else:
                l.id_franchise = u.id_franchise
                l.active = True
                l.used = True
                l.save()
                f_name = l.id_provider.nombre
                success = 1
        except:
            success = 0
    return render(request, 'link_provider/link_with_provider.html', {
            'usuario' : u,
            'success' : success,
            'code' : code,
            'franchise_name' : f_name
            })

@login_required
def my_providers(request):
    empty_list = 0
    u = OCSUser.objects.get(user = request.user)
    relation_list = LinkWithF.objects.filter(id_franchise=u.id_franchise.id)
    if len(relation_list) == 0:
        empty_list = 1

    return render(request, 'my_providers/consult_providers.html', {
            'usuario' : u,
            'relation_list' : relation_list,
            'empty_list' : empty_list
            })


@login_required
def provider_detail(request, id_provider):
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

    return render(request, 'my_providers/provider_detail.html', {
            'usuario' : u,
            'success' : success,
            'provider' : p,
            })


# function that displays the table of the franchise inventory
# Input: the request method with the values of the session
# Output: the inventory of the franchise
@login_required
def show_inventory(request):
    empty_field = 0
    amount_error = 0
    product_already_exists = 0
    registration_success = 0

    u = OCSUser.objects.get(user = request.user)
    product_list = PrivateProduct.objects.filter(id_franchise=u.id_franchise.id)


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













#
