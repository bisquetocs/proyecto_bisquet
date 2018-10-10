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

from .models import Provider

@login_required
def registerProvider(request):
    if request.method == 'POST':
        register_form = RegisterProviderForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            return render(request, 'provider/register.html', {'Success_mesage': result})
    else:
        u = OCSUser.objects.get(user = request.user)
        if u.id_provider!=None:
            return redirect('../provider/infoProvider')
        elif u.id_provider==None and (u.id_franchise!=None):
            return redirect('../franchise/infoFranchise')
        else:
            register_form = RegisterProviderForm()
            return render(request, 'provider/register.html', {'register_form': register_form})
@login_required
def infoProvider(request):
    u = OCSUser.objects.get(user = request.user)
    if u.id_provider!=None:
        return render(request, 'provider/info.html')
    else:
        return redirect('../')



























#
