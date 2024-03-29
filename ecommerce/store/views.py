from django.shortcuts import render, redirect
from .models import *


def homepage(request):
    banners = Banner.objects.filter(active=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def store(request, category_name=None):
    products = Product.objects.filter(active=True)
    if category_name:
        products = products.filter(category__name=category_name)
    context = {"products": products}
    return render(request, 'store.html', context)


def see_product(request, id_product, id_color=None):
    there_is_stok = False
    colors = {}
    sizes = {}
    selected_color=None         
    
    if id_color:
        selected_color = Color.objects.get(id=id_color)
    product = Product.objects.get(id=id_product)
    stok_item = StokItem.objects.filter(product=product, quantity__gt=0)
    if len(stok_item) > 0:
        there_is_stok = True
        colors = {item.color for item in stok_item}
        if id_color:
            stok_item = StokItem.objects.filter(product=product, quantity__gt=0, color__id=id_color)
            sizes = { item.size for item in stok_item }
   
    context = {"product": product, "there_is_stok": there_is_stok, "colors": colors, "sizes": sizes, "selected_color": selected_color}
    return render(request,'see_product.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, done=False)
    order_items = OrderItem.objects.filter(order=order)
    context = {"order_items": order_items, "order": order }
    return render(request, 'cart.html', context)


def addto_cart(request, id_product):
    if request.method == 'POST' and id_product:
        data = request.POST.dict()
        size = data.get("size")
        id_color = data.get("color")
        
        if not size or not id_color:
            return redirect('store')
        
        # taking customer
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            return redirect('store')
        
        order, created = Order.objects.get_or_create(customer=customer, done=False)
        stok_item = StokItem.objects.get(product__id=id_product, size=size, color__id=id_color)        
        order_items, created = OrderItem.objects.get_or_create(stok_item=stok_item, order=order)
        order_items.quantity += 1
        order_items.save()
        return redirect('cart')
    else:
        return redirect('store')
    
    
    
def remove_cart(request, id_product):
    if request.method == 'POST' and id_product:
        data = request.POST.dict()
        size = data.get("size")
        id_color = data.get("color")
        
        if not size or not id_color:
            return redirect('store')
        
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            return redirect('store')
        
        order, created = Order.objects.get_or_create(customer=customer, done=False)
        stok_item = StokItem.objects.get(product__id=id_product, size=size, color__id=id_color)        
        order_items, created = OrderItem.objects.get_or_create(stok_item=stok_item, order=order)
        order_items.quantity -= 1
        order_items.save()
        
        if order_items.quantity <= 0:
            order_items.delete()
        return redirect('cart')
    else:
        return redirect('store')
        


def checkout(request):
    return render(request, 'checkout.html')



#USER:
def account(request):
    return render(request, 'user/account.html')


def login(request):
    return render(request, 'user/login.html')