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

from .models import Provider, LinkWithF, Days, OfficeHours

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
    prov = Provider.objects.get(id = u.id_provider.id)
    prod = Product.objects.filter(id_provider = prov.id)
    if u.id_provider!=None:
        return render(request, 'provider/home.html', {'usuario':u, 'productos':prod,})
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


@login_required
def office(request):
    u = OCSUser.objects.get(user = request.user)
    prov = u.id_provider_id
    provider = Provider.objects.get(id = prov)

    days_list = Days.objects.all()
    hours_list = OfficeHours.objects.filter(id_provider = provider)

    if request.method == 'POST':

        for item in days_list:
            i = item.id
            s_hour = "start_hour_" + str(i)
            f_hour = "finish_hour_" + str(i)
            edit_object = OfficeHours.objects.get(day = item, id_provider = provider)
            edit_object.start_hour = request.POST[s_hour]
            edit_object.finish_hour = request.POST[f_hour]
            edit_object.save()

    return render(request, 'provider/office.html', {'days_list':days_list, 'hours_list': hours_list})
