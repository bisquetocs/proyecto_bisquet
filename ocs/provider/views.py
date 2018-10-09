# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from .forms import RegisterProviderForm

from .models import Provider

@login_required
def registerProvider(request):
    if request.method == 'POST':
        register_form = RegisterProviderForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            return render(request, 'provider/register.html', {'Success_mesage': result})

    else:
        register_form = RegisterProviderForm()
    return render(request, 'provider/register.html', {'register_form': register_form})
    #razon_social = request.POST
    #rfc = request.POST['rfc']
    #p = proveedor(question_text="What's new?", pub_date=timezone.now())
    #return 0
