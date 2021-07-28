from accounts import views
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('product/', views.productsPage, name = "product"),
    path('register/', views.register, name="registerpage"),
    path('login/', views.loginPage, name="loginpage"),
    path('user/', views.userPage, name = "userpage"),
    path('logout/', views.logoutUser, name="logoutpage"),
    path('customer/<str:pk_test>/', views.customerPage, name="customer"),
    path('create_order/<str:pkCrteOrder>', views.createOrder, name = "create_order"),
    path('update_order/<str:pkOrderForm>', views.updateOrder, name = "update_order"),
    path('delete_order/<str:toDel>', views.deleteOrder, name = "delete_order"),

]
