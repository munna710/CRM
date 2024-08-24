from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def products(request):
    return render(request, 'accounts/product.html')

def customers(request):
    return render(request, 'accounts/customer.html')