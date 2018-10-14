from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import RegisterFranchiseForm
from provider.models import LinkWithF
from accounts.models import OCSUser

from .models import Franchise

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

    return render(request, 'my_providers/consult_providers.html', {
            'usuario' : u,
            'relation_list' : relation_list,
            'empty_list' : empty_list
            })

























#
