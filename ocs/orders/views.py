from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from accounts.models import OCSUser
from provider.models import Provider
from provider.models import LinkWithF
from franchise.models import Franchise

from django.http import JsonResponse
import json


def make_order(request):
    u = OCSUser.objects.get(user = request.user)
    franchise = Franchise.objects.get(id = u.id_franchise.id)
    my_providers = LinkWithF.objects.filter(id_franchise = franchise, active = True)
    return render(request, 'orders/make_order.html', {'usuario':u,'franchise':franchise,})

















#
