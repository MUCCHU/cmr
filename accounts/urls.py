from accounts import views
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('product/', views.productsPage, name = "product"),
    path('customer/<str:pk_test>/', views.customerPage, name="customer"),
    path('create_order/<str:pkCrteOrder>', views.createOrder, name = "create_order"),
    path('update_order/<str:pkOrderForm>', views.updateOrder, name = "update_order"),
    path('delete_order/<str:toDel>', views.deleteOrder, name = "delete_order"),

]
