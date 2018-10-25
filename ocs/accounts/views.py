from django.shortcuts import render, redirect
from django.contrib.auth.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db.models import Q
from accounts.models import OCSUser, IsProviderOrFranchise

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('../accounts/locate')
    else:
        return render(request, 'accounts/landing.html')

def registerUser(request):
    """
     Function used to register a user to the database
     INPUT
        - Request method with the values of the session and the
          values sended by POST
     OUTPUT
        - A response with the status of the registration
    """
    if request.method == 'POST':
        uname = request.POST['username']
        fName = request.POST['firstName']
        lName = request.POST['lastName']
        em = request.POST['email']
        passwd = request.POST['password']
        cpasswd = request.POST['confpass']
        role = "Empleado generico"
        if (uname==''  or fName=='' or lName=='' or em=='' or passwd=='' or cpasswd=='' or role==''):
            return render(request, 'registration/register.html', {
                'emptyField' : 1
            })
        if (passwd != cpasswd):
            return render(request, 'registration/register.html', {
                'passConfirmError' : 1
            })
        nu = User(username=uname, first_name=fName, last_name=lName, email=em)
        nu.set_password(passwd)
        userTest = User
        # Check if username already exists
        try:
            userTest = User.objects.get(username=nu.username)
        except userTest.DoesNotExist:
            nu.save()
            g = Group.objects.get(name=role)
            g.user_set.add(nu)
            g.save()
            ocsUser = OCSUser(user=nu)
            ocsUser.save()
            # Redirect to home
            messages.info(request, 'Registro exitoso')
            return redirect('../')
        else:
            # Reload the form if the user already exists
            return render(request, 'registration/register.html', {
                'userAlreadyExists' : 1
            })
    else:
        return render(request, 'registration/register.html')

@login_required
def locate(request):
    ocs_user = OCSUser.objects.get(user = request.user)
    if ocs_user.id_provider == None and ocs_user.id_franchise == None:
        return render(request, 'home/index.html', {'usuario':request.user})
    elif ocs_user.id_provider != None:
        return redirect(reverse('provider:home'))
    elif ocs_user.id_franchise != None:
        return redirect(reverse('franchise:home'))

@login_required
def misEmpleados(request):
    ocs_user = OCSUser.objects.get(user = request.user)
    if ocs_user.id_provider is None:
        #Es franchise
        aux = "franchise/home.html"
        empleados_list = OCSUser.objects.filter(id_franchise=ocs_user.id_franchise, active = 1)
    elif ocs_user.id_franchise is None:
        #Es provider
        aux = "provider/home.html"
        empleados_list = OCSUser.objects.filter(id_provider=ocs_user.id_provider, active = 1)
    else:
        #Somos nosotros viendo a todos los que están registrados
        empleados_list = OCSUser.objects.all()
    return render(request, 'empleados/misEmpleados.html', {'usuario':ocs_user,'empleados_list':empleados_list,'aux':aux})

@login_required
def registrarEmpleado(request):
    ocs_user = OCSUser.objects.get(user = request.user)
    if request.method == 'POST':
        try:
            employee = User.objects.get(username = request.POST['inputUser'])
        except (KeyError, User.DoesNotExist):
            messages.info(request, 'El usuario no existe')
            return redirect('../myEmployees')
        else:
            ocs_employee = OCSUser.objects.get(user = employee)
            if ocs_employee.id_provider == None and ocs_employee.id_franchise == None:
                employee_group = User.groups.through.objects.get(user = employee)
                grp = request.POST['inputRol']
                ocs_employee.id_provider = ocs_user.id_provider
                ocs_employee.save()
                employee_group.group = Group.objects.get(name = grp)
                employee_group.save()
                messages.info(request, 'Registro exitoso!')
            else:
                messages.info(request, 'El empleado ya está registrado')
            return redirect('../myEmployees')
    else:
        if ocs_user.id_provider is None: #Es franchise
            aux = "franchise/home.html"
            rolesf = IsProviderOrFranchise.objects.exclude(is_franchise=True)
            roles = Group.objects.filter(~Q(id__in=rolesf))
            empleados_list = OCSUser.objects.filter(id_franchise=ocs_user.id_franchise, active = 1)
        elif ocs_user.id_franchise is None: #Es provider
            aux = "provider/home.html"
            rolesp = IsProviderOrFranchise.objects.exclude(is_provider=True)
            roles = Group.objects.filter(~Q(id__in=rolesp))
            empleados_list = OCSUser.objects.filter(id_provider=ocs_user.id_provider, active = 1)
        return render(request, 'empleados/registrarEmpleado.html', {'usuario':ocs_user,'empleados_list':empleados_list,'groups_list':roles,'aux':aux})

@login_required
def borrarEmpleado(request, emp_id):
    ocs_user = OCSUser.objects.get(user = request.user)

    ##Descativa permisos de inicio de sesión de Django sin borrar
    del_object = User.objects.get(id = emp_id)
    del_object.is_active = 0
    del_object.save()

    #Desactiva usuario, cambia estado
    del_user = OCSUser.objects.get(user = emp_id)
    del_user.active = 0;
    del_user.save()

    messages.info(request, 'Borrado exitoso!')

    return redirect('../')

@login_required
def verEmpleado(request, emp_id):
    ocs_user = OCSUser.objects.get(user = request.user)
    request_user = OCSUser.objects.get(user = emp_id)
    ocs_group = User.groups.through.objects.get(user = emp_id)
    id_group = ocs_group.group
    group = Group.objects.get(name = id_group)
    if request.method == 'POST':
        grp = request.POST['role']
        ocs_group.group = Group.objects.get(name = grp)
        ocs_group.save()
        url = '../verEmpleado/' + str(emp_id)
        return redirect(url)

    else:
        if ocs_user.id_provider is None: #Es franchise
            aux = "franchise/home.html"
            rolesf = IsProviderOrFranchise.objects.exclude(is_franchise=True)
            roles = Group.objects.filter(~Q(id__in=rolesf))

        elif ocs_user.id_franchise is None: #Es provider
            aux = "provider/home.html"
            rolesp = IsProviderOrFranchise.objects.exclude(is_provider=True)
            roles = Group.objects.filter(~Q(id__in=rolesp))

    return render(request, 'empleados/verEmpleado.html',{'aux':aux, 'group':group, 'role_list':roles, 'employee':request_user, 'usuario':ocs_user})

#
