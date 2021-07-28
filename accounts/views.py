from django.contrib.auth import authenticate, login, logout
from django.db.models import fields
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse, request
from .models import *
from .forms import orderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.

@login_required(login_url='loginpage')
@admin_only
def home(request):
    orders = order.objects.all()
    CusList = customer.objects.all()
    total_customers = CusList.count()
    total_orders = orders.count()
    deliverd = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context ={'orders':orders, 'customers': CusList, 'totalOrders': total_orders, 'delivered':deliverd, 'pending': pending }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    deliverd = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'totalOrders': total_orders, 'delivered':deliverd, 'pending': pending }
    return render(request, "accounts/userpage.html", context)
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    context = {"form": form}
    if(request.method=="POST"):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer.objects.create(
                user=user,
            )
            username =form.cleaned_data.get("username")
            messages.success(request,"Account was created successfully for "+username)
            return redirect("loginpage")
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if(request.method=="POST"):
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username = username, password= password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "username or password is incorrect")

        return render(request, 'accounts/login.html')
def logoutUser(request):
    logout(request)
    return redirect("loginpage")


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def productsPage(request):
    productList = products.objects.all()
    return render(request, 'accounts/products.html', {'Products': productList})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def customerPage(request, pk_test):
    NewCustomer = customer.objects.get(id = pk_test)
    orders = NewCustomer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders);
    orders = myFilter.qs

    context = {'customer': NewCustomer, 'orders': orders, 'Order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pkCrteOrder):
    OrderFormSet = inlineformset_factory(customer, order, fields=('product','status'), extra=7)
    CustomerOrderOwner = customer.objects.get(id=pkCrteOrder)
    #form = orderForm(initial={'customer' : CustomerOrderOwner })
    formSet = OrderFormSet(queryset = order.objects.none(), instance=CustomerOrderOwner)
    if(request.method == 'POST'): 
        # print("Printing request\n", request.POST)
        # form = orderForm(request.POST)
        print("post request detected")
        formSet = OrderFormSet(request.POST, instance=CustomerOrderOwner)
        if formSet.is_valid():
            formSet.save()
            print("Trying to redirect to / ")
            return(redirect('/'))
        else:
            print("formset was invalid")

    context = {'formSet': formSet}
    return(render(request, 'accounts/orderForm.html', context))


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pkOrderForm):
    orderPa = order.objects.get(id = pkOrderForm)

    form = orderForm(instance=orderPa)
    if(request.method == 'POST'):
            form = orderForm(request.POST, instance=orderPa)
            if form.is_valid():
                form.save()
                return(redirect('/'))
    context = {'orderform': form}
    return(render(request, 'accounts/orderForm.html', context))


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, toDel):
    orderToDelete = order.objects.get(id = toDel)
    context = {'item': orderToDelete}
    if(request.method == 'POST'):
        orderToDelete.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)
