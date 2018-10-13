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

from .models import Provider

@login_required
def registerProvider(request):
    if request.method == 'POST':
        register_form = RegisterProviderForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
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
    return render(request, 'link_code/generate_link.html')


























#
