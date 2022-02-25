from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import LoginForm
from .models import *


class Index(View):
    template = 'ecom/index.html'

    def get_context_data(self, request):
        try:
            products = Product.objects.get_queryset()
        except Product.DoesNotExist:
            products = None
        return {'products': products, 'user': request.user}

    def get(self, request):
        return render(request, self.template, self.get_context_data(request))

    def post(self, request):
        product = Product.objects.get(id=request.POST.get("product"))
        try:
            product_in_cart = ProductInCart.objects.get(product=product)
            product_in_cart.add_to_cart()
            product_in_cart.save( )
        except ProductInCart.DoesNotExist:
            ProductInCart.objects.create(product=product).save()
        return redirect('index')


class Cart(View):

    def get_context_data(self, request):
        products_in_cart = ProductInCart.objects.get_queryset()
        total = self.get_cart_total(products_in_cart)
        return {'products': products_in_cart, 'total': total}

    def get(self, request):
        return render(request, 'ecom/cart.html', self.get_context_data(request))

    def post(self, request):
        if request.POST.get("delete"):
            product_in_cart = ProductInCart.objects.filter(id=request.POST.get("delete")).get()
            product_in_cart.product.quantity += product_in_cart.quantity
            product_in_cart.product.save()
            product_in_cart.delete()
        return redirect('cart')

    def get_cart_total(self, products_in_cart):
        total = 0
        for product in products_in_cart:
            total += product.get_total_price()
        return total


def checkout(request):
    pass


def signup(request):
    context = {}
    form = UserCreationForm(request.POST)
    context['form'] = form
    if request.method == "POST":
        if form.is_valid:
            form.save()
            return redirect('index')
    return render(request, 'ecom/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user=user)
                    return redirect('index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'ecom/login.html', {'form': form})


def product_page(request, id):
    product = Product.objects.get(id=id)
    context = {'product':product}
    return render(request, 'ecom/product_page.html', context)
