from django.db.models import fields
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse, request
from .models import *
from .forms import orderForm
from .filters import OrderFilter
# Create your views here.


def home(request):
    orders = order.objects.all()
    CusList = customer.objects.all()
    total_customers = CusList.count()
    total_orders = orders.count()
    deliverd = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context ={'orders':orders, 'customers': CusList, 'totalOrders': total_orders, 'delivered':deliverd, 'pending': pending }
    return render(request, 'accounts/dashboard.html', context)


def productsPage(request):
    productList = products.objects.all()
    return render(request, 'accounts/products.html', {'Products': productList})


def customerPage(request, pk_test):
    NewCustomer = customer.objects.get(id = pk_test)
    orders = NewCustomer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter();

    context = {'customer': NewCustomer, 'orders': orders, 'Order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)

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

def deleteOrder(request, toDel):
    orderToDelete = order.objects.get(id = toDel)
    context = {'item': orderToDelete}
    if(request.method == 'POST'):
        orderToDelete.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context)
