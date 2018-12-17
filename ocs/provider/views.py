"""
created by:     Django
description:    This are the views of the providers that helps their tasks
                to accomplish
modify by:      Fatima
modify date:    12/11/18
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


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
            provider = register_form.process_registration(request.user)
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
    francs = LinkWithF.objects.filter(id_provider = u.id_provider, used = False)
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
            'code' : code,
            'francs' : francs,
            })

#Función para asignar horas de oficina a la empresa de lado proveedor
@login_required
def office_assign(request, id_day_hour):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)
    days_hour = OfficeHours.objects.get(id = id_day_hour)
    hours_list = OfficeHours.objects.filter(id_provider = provider)
    prov = Group.objects.get(name = "Administrador de empresa")
    user = request.user
    if request.method == 'POST' and (prov in user.groups.all()):
        #En lugar de añadir más filas a la tabla, sólo se editan las ya existentes
        days_hour.start_hour = request.POST["s_hour"]
        days_hour.finish_hour = request.POST["f_hour"]
        days_hour.save()

        return render(request, 'provider/office_main.html', {'hours_list': hours_list, 'usuario':u})

    #Only owners can perform the action
    if (prov in user.groups.all()):
        return render(request, 'provider/office.html', {'days_hour':days_hour, 'usuario':u})
    else :
        return redirect('../')

@login_required
def office(request):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)
    hours_list = OfficeHours.objects.filter(id_provider = provider)
    prov = Group.objects.get(name = "Administrador de empresa")
    user = request.user

    #Only owners can perform the action
    if (prov in user.groups.all()):
        return render(request, 'provider/office_main.html', {'hours_list': hours_list, 'usuario':u})
    else :
        return redirect('../')


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
    user = request.user
    u = OCSUser.objects.get(user = user)
    prov = u.id_provider
    #provider = Provider.objects.get(id = prov.id)
    group_prov = Group.objects.get(name = "Administrador de empresa")

    #Selecciona la lista de los días
    days_list = Days.objects.all()

    lun = Days.objects.get(nombre="Lunes")
    lunes = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = lun, activo=True)
    mar = Days.objects.get(nombre="Martes")
    martes = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = mar, activo=True)
    mie = Days.objects.get(nombre="Miércoles")
    miercoles = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = mie, activo=True)
    jue = Days.objects.get(nombre="Jueves")
    jueves = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = jue, activo=True)
    vie = Days.objects.get(nombre="Viernes")
    viernes = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = vie, activo=True)
    sab = Days.objects.get(nombre="Sábado")
    sabado = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = sab, activo=True)
    dom = Days.objects.get(nombre="Domingo")
    domingo = DailyClients.objects.values_list('id_franchise', flat=True).filter(id_provider = prov, day = dom, activo=True)

    #Se hace un filtro para desplegar solo los clientes ligados con ese usuario proveedor
    clients_list = LinkWithF.objects.filter(id_provider = prov, active=True)

    data = {    'usuario':u,
                'clients_list': clients_list,
                'days_list':days_list,
                'lunes':lunes,
                'martes':martes,
                'miercoles':miercoles,
                'jueves':jueves,
                'viernes':viernes,
                'sabado':sabado,
                'domingo':domingo,
                }
    if request.method == 'POST' and (group_prov in user.groups.all()):
        #Hace el registro
        obj_prov = prov
        obj_fran = Franchise.objects.get( nombre = request.POST['client'])
        obj_day = Days.objects.get(nombre = request.POST['day'])

        daily_clients = DailyClients.objects.filter(id_provider = prov, activo=True)
        aux = False
        for d in daily_clients:
            if d.id_franchise == obj_fran and d.day == obj_day:
                aux = True
                messages.warning(request, '¡Esa relación ya existe!')

        if aux is False:
            register = DailyClients(id_provider = obj_prov, id_franchise = obj_fran, day = obj_day, activo = True)
            register.save()
            messages.success(request, 'Tu cliente ya te podrá pedir estos días...')
        #Fin de registro
        return redirect(reverse('provider:daily_clients'))
    if (group_prov in user.groups.all()):
        return render(request, 'my_clients/daily_clients.html', data)
    else:
        return redirect('../')

def daily_clients_interactive(request):
    user = request.user
    u = OCSUser.objects.get(user = user)
    prov = u.id_provider
    id_franchise = request.GET.get('id_franchise', None)
    day = request.GET.get('day', None)
    add = request.GET.get('add', None)
    if id_franchise is not None and day is not None and add is not None:
        obj_prov = prov
        obj_fran = Franchise.objects.get(id = id_franchise)
        obj_day = Days.objects.get(id = day)
        daily_clients = DailyClients.objects.filter(id_provider = prov, activo=True)
        for d in daily_clients:
            if d.id_franchise == obj_fran and d.day == obj_day:
                d.activo = False
                d.save()
                d.delete()
                messages.warning(request, 'Tu cliente ya NO te podrá pedir estos días... (Solo pedidos emergentes)')
        if add == 'true':
            register = DailyClients(id_provider = obj_prov, id_franchise = obj_fran, day = obj_day, activo = True)
            register.save()
            messages.success(request, 'Tu cliente ya te podrá pedir estos días...')
        data = { 'success': True, }
        return JsonResponse(data)

# Function that shows the Provider company profile
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
