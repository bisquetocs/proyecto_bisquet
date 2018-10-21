from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import RegisterProviderForm
from accounts.models import OCSUser
from products.models import Product
from franchise.models import Franchise

from .models import Provider, LinkWithF, Days, OfficeHours, DailyClients

import string
import random

def code_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required
def registerProvider(request):
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
            return render(request, 'provider/home.html')
    else:
        u = OCSUser.objects.get(user = request.user)
        if u.id_provider!=None:
            return redirect('../provider/home')
        elif u.id_provider==None and (u.id_franchise!=None):
            return redirect('../franchise/home')
        else:
            register_form = RegisterProviderForm()
            return render(request, 'provider/register.html', {'register_form': register_form})

@login_required
def home(request):
    u = OCSUser.objects.get(user = request.user)
    if u.id_provider!=None:
        return render(request, 'provider/home.html', {'usuario':u,})
    else:
        return redirect('../')

@login_required
def link_code(request):
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

    return render(request, 'provider/office.html', {'days_list':days_list, 'hours_list': hours_list, 'usuario':u})

@login_required
def clients(request):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)


    return render(request, 'clients/main.html', {'usuario':u})

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


    return render(request, 'clients/daily_clients.html', {'usuario':u, 'clients_list': clients_list, 'days_list':days_list})
