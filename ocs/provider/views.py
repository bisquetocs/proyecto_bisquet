"""
created by:     Django
description:    This are the views of the providers that helps their tasks
                to accomplish
modify by:      Alberto
modify date:    26/10/18
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

from .forms import RegisterProviderForm
from accounts.models import OCSUser
from products.models import Product
from franchise.models import Franchise

from .models import Provider, LinkWithF, Days, OfficeHours, DailyClients

import string
import random

# Function that generates a random code of 12 characters
def code_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Function that registers a new provider
@login_required
def registerProvider(request):
    # If POST then register provider
    if request.method == 'POST':
        register_form = RegisterProviderForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            days_list = Days.objects.all()
            ##Inicia - Asigna horas de oficina por default
            for item in days_list:
                insert = OfficeHours(start_hour = "8:00", finish_hour = "18:00", day = item, id_provider = provider)
                insert.save()
            ##Termina
            return redirect('/accounts/locate/')
    # If not POST then show registration form
    else:
        u = OCSUser.objects.get(user = request.user)
        if u.id_provider!=None:
            return redirect('../provider/home')
        elif u.id_provider==None and (u.id_franchise!=None):
            return redirect('../franchise/home')
        else:
            register_form = RegisterProviderForm()
            return render(request, 'provider/register.html', {'register_form': register_form})

# Function that shows the homepage of provider
@login_required
def home(request):
    u = OCSUser.objects.get(user = request.user)
    if u.id_provider!=None:
        # Show provider home
        return render(request, 'provider/home.html', {'usuario':u,})
    else:
        # Redirect to other home
        return redirect('../')

@login_required
def link_code(request):
    """
     Function used to generate a random code to link with a franchise
     INPUT
        - Request method with the values of the session & the values
          sended by a POST method
     OUTPUT
        - A random code already saved in the database
    """
    u = OCSUser.objects.get(user = request.user)
    code = ''
    if request.method == 'POST':
        code = code_generator()
        l = LinkWithF(link_code=code, used=False, active=False)
        try:
            lTest = LinkWithF.objects.get(link_code=code)
        except:
            l.id_provider=u.id_provider
            l.save()
        else:
            link_code(request)
    return render(request, 'link_code/generate_link.html', {
            'usuario' : u,
            'code' : code
            })

#Función para asignar horas de oficina a la empresa de lado proveedor
@login_required
def office(request):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)
    days_list = Days.objects.all()
    hours_list = OfficeHours.objects.filter(id_provider = provider)
    if request.method == 'POST':
        #La asignación se hace dentro de un ciclo for pues se asigna a cada día
        for item in days_list:
            i = item.id
            s_hour = "start_hour_" + str(i)
            f_hour = "finish_hour_" + str(i)
            #En lugar de añadir más filas a la tabla, sólo se editan las ya existentes
            edit_object = OfficeHours.objects.get(day = item, id_provider = provider)
            edit_object.start_hour = request.POST[s_hour]
            edit_object.finish_hour = request.POST[f_hour]
            edit_object.save()
            return redirect('/provider/office/')
    return render(request, 'provider/office.html', {'days_list':days_list, 'hours_list': hours_list, 'usuario':u})

@login_required
def my_clients(request):
    empty_list = 0
    u = OCSUser.objects.get(user = request.user)
    relation_list = LinkWithF.objects.filter(id_provider=u.id_provider.id, active=True)
    if len(relation_list) == 0:
        empty_list = 1
    return render(request, 'my_clients/consult_clients.html', {'usuario' : u,'relation_list' : relation_list,'empty_list' : empty_list})

# Function that shows the provider its client detail
@login_required
def client_detail(request, id_franchise):
    success = True
    u = OCSUser.objects.get(user = request.user)
    F = Franchise()
    relation_list = LinkWithF.objects.filter(id_provider=u.id_provider, id_franchise=id_franchise)
    try:
        f = Franchise.objects.get(id=id_franchise)
        if len(relation_list) == 0:
            success = False
    except:
        success = False
    return render(request, 'my_clients/client_detail.html', {'usuario' : u,'success' : success,'franchise' : f,})

#Función para desplegar y añadir los clientes diarios de una empresa del lado de proveedor
@login_required
def daily_clients(request):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)
    #Selecciona la lista de los días
    days_list = Days.objects.all()
    #Se hace un filtro para desplegar solo los clientes ligados con ese usuario proveedor
    fran_prov = LinkWithF.objects.values_list('id_franchise', flat=True).filter(id_provider = prov)
    clients_list = Franchise.objects.filter(id__in = fran_prov)
    if request.method == 'POST':
        #Hace el registro
        obj_fran =  Franchise.objects.get( nombre = request.POST['client'])
        obj_day = Days.objects.get(nombre = request.POST['day'])

        register = DailyClients(franchise = obj_fran, day = obj_day, status = 'Sin pedido')
        register.save()
        #Fin de registro
    return render(request, 'my_clients/daily_clients.html', {'usuario':u, 'clients_list': clients_list, 'days_list':days_list})

# Function that shows the Provider comppany profile
@login_required
def profile (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    return render(request, 'provider/profile.html', {'usuario':ocs_user,})

# Function that let the providers to edit its company info
@login_required
def edit_provider (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    # If POST then edit provider
    if request.method == 'POST':
        p = Provider.objects.get(id=ocs_user.id_provider.id)
        p.nombre=request.POST['nombre']
        p.razon_social=request.POST['razon_social']
        p.rfc=request.POST['rfc']
        p.domicilio=request.POST['domicilio']
        p.mision=request.POST['mision']
        p.vision=request.POST['vision']
        p.save()
        messages.success(request, 'La información se actualizó con éxito!')
        return redirect(reverse('provider:profile'))
    # If not POST then shows edit_provider form
    else:
        return render(request, 'provider/profile.html', {'usuario':ocs_user, 'edit':True,})






#
