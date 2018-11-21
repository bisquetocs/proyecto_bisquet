"""
Created by : Django
Description: Views file for the Franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .forms import RegisterFranchiseForm
from provider.models import LinkWithF, Provider
from accounts.models import OCSUser
from orders.models import Order

from .models import Franchise


from datetime import datetime, timedelta

@login_required
def registerFranchise(request):
    if request.method == 'POST':
        register_form = RegisterFranchiseForm(request.POST)
        if register_form.is_valid():
            result = register_form.process_registration(request.user)
            return redirect('/accounts/locate/')
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
        return render(request, 'home_reports/reports.html', {'usuario':u,})
    else:
        return redirect('../')


@login_required
def get_light_reports(request):
    """
    By: DanteMaxF
     Function used to send in a json format
     INPUT
        - Request method with the values of the session
     OUTPUT
        - A Json response with the values needed for the dashboard
    """
    u = OCSUser.objects.get(user = request.user)
    background_color_pool = ["#F39C12", "#011F45","#FF4040","#34A853","#4285F4", "#011F45","#FF4040","#1A457A","#F39C12", "#011F45","#FF4040","#1A457A"]
    # Data for the number of orders in the last 5 days
    days_ago = 5
    days = []
    days_aux = []
    orders_by_day = []

    order_list = Order.objects.filter(id_franchise = u.id_franchise)
    for i in range(days_ago, 0, -1):
        days_aux.append( ((datetime.now() - timedelta(days=i)).date()) )
        days.append((datetime.now()-timedelta(days=i)).strftime("%d/%b/%y"))
    days.append('Today')
    days_aux.append(datetime.now())
    for i in range(0,days_ago+1):
        orders_by_day.append(Order.objects.filter(id_franchise = u.id_franchise, fecha_pedido__range=(days_aux[i] - timedelta(days=1), days_aux[i])).count())


    # Data for the number of orders per provider

    count_providers = order_list.values('id_provider').annotate(dcount=Count('id_provider'))
    prov_names = []
    prov_num_orders = []
    prov_colors = []
    for i in range(0, len(count_providers)):
        prov_names.append( (Provider.objects.get(id=count_providers[i]['id_provider'])).nombre )
        prov_num_orders.append( count_providers[i]['dcount'] )
        prov_colors.append( background_color_pool[i] )



    total_inversion = []
    for j in range(0, len(count_providers)):
        aux_sum = 0
        prov_obj = Provider.objects.get(id=count_providers[j]['id_provider'])
        orders_by_prov = Order.objects.filter(id_provider = prov_obj)
        for order in orders_by_prov:
            aux_sum = aux_sum + order.precio_total
        total_inversion.append(float(aux_sum))


    #Json response
    data = {
        "days": days,
        "orders_by_day": orders_by_day,

        "provider_names": prov_names,
        "provider_num_orders": prov_num_orders,
        "provider_color": prov_colors,
        "total_inversion": total_inversion,
    }
    return JsonResponse(data)


@login_required
def link_provider(request):
    """
    By: DanteMaxF
     Function used to link a franchise with a provider using a link code
     INPUT
        - Request method with the values of the session
        - A post method with the link code inserted by the user
     OUTPUT
        - A reload of the same page and a response of the status of the process
    """
    u = OCSUser.objects.get(user = request.user)
    code = ''
    f_name = ''
    if request.method == 'POST':
        code = request.POST['link_code']
        try:
            l = LinkWithF.objects.get(link_code=code)
            print(l.date_of_creation)
            if l.used or l.check_timeout():
                messages.warning(request, 'El código ya fue utilizado o caducado, por favor, solicita a tu proveedor que te genere un código nuevo.')
            else:
                l.id_franchise = u.id_franchise
                l.active = True
                l.used = True
                l.save()
                f_name = l.id_provider.nombre
                messages.success(request, '¡EXITO! Te has relacionado con '+f_name)
        except:
            messages.error(request, 'El código no coincide con ninguno registrado, ingrésalo de nuevo o consulta a tu proveedor..')
    return render(request, 'link_provider/link_with_provider.html', {
            'usuario' : u,
            'code' : code,
            'franchise_name' : f_name
            })

@login_required
def my_providers(request):
    """
    By: DanteMaxF
     Function used to display the providers linked with the user using the system
     INPUT
        - Request method with the values of the session
     OUTPUT
        - Query set with the list of providers
    """
    empty_list = 0
    u = OCSUser.objects.get(user = request.user)
    relation_list = LinkWithF.objects.filter(id_franchise=u.id_franchise)
    if len(relation_list) == 0:
        empty_list = 1

    return render(request, 'my_providers/consult_providers.html', {
            'usuario' : u,
            'relation_list' : relation_list,
            'empty_list' : empty_list
            })


@login_required
def provider_detail(request, id_provider):
    """
    By: DanteMaxF
     Function that displays the details of the provider selected in the provider table
     INPUT
        - Request method with the values of the session
        - Id of the provider to consult_providers
     OUTPUT
        - Detailed information of each attribute from the provider
    """
    success = True
    u = OCSUser.objects.get(user = request.user)
    p = Provider()
    relation_list = LinkWithF.objects.filter(id_franchise=u.id_franchise, id_provider=id_provider)
    try:
        p = Provider.objects.get(id=id_provider)
        if len(relation_list) == 0:
            success = False
    except:
        success = False
        raise Http404("Provider does not exist")
    return render(request, 'my_providers/provider_detail.html', {
            'usuario' : u,
            'success' : success,
            'provider' : p,
            })


@login_required
def profile (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    return render(request, 'franchise/profile.html', {'usuario':ocs_user,})

@login_required
def edit_franchise (request):
    ocs_user = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        f = Franchise.objects.get(id=ocs_user.id_franchise.id)
        f.nombre=request.POST['nombre']
        f.razon_social=request.POST['razon_social']
        f.rfc=request.POST['rfc']
        f.domicilio=request.POST['domicilio']
        f.save()
        messages.success(request, 'La información se actualizó con éxito!')
        return redirect(reverse('franchise:profile'))
    else:
        return render(request, 'franchise/profile.html', {'usuario':ocs_user, 'edit':True,})










#
