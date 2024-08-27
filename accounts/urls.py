from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('user/', views.userPage, name='user'),
    path('account/', views.accountSettings, name='account'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customers'),
    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

]
