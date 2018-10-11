from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import RegisterFranchiseForm

from .models import Franchise

@login_required
def registerFranchise(request):
    if request.method == 'POST':
        register_form = RegisterFranchiseForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            return render(request, 'franchise/register.html', {'Success_mesage': result})

    else:
        register_form = RegisterFranchiseForm()
    return render(request, 'franchise/register.html', {'register_form': register_form})
