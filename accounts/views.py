from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            
            
            return redirect('login')
    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        
        else:
            messages.info(request, "username or password is incorrect")
    
    context = {'form':form}
    return render(request, 'accounts/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'accounts/product.html',context)

@login_required(login_url='login')
def customers(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    
    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'my_filter':my_filter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'item':order}
    return render(request, 'accounts/delete_item.html', context)