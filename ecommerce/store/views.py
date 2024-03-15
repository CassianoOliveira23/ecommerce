from django.shortcuts import render
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
    color_selected=None         #reassistir aula  27 e corrigir os erros
    
    if id_color:
        color = Color.get(id=id_color)
        color_selected = color.name
    product = Product.objects.get(id=id_product)
    stok_item = StokItem.objects.filter(product=product, quantity__gt=0)# gt: Greater than
    if len(stok_item) > 0:
        there_is_stok = True
        colors = {item.color for item in stok_item}
        if id_color:
            stok_item = StokItem.objects.filter(product=product, quantity__gt=0, color__id=id_color)
            sizes = { item.size for item in stok_item }
   
    context = {"product": product, "stok_item": stok_item, "there_is_stok": there_is_stok, "colors": colors, "size": sizes, "color_selected": color_selected}
    return render(request,'see_product.html', context)


def cart(request):
    return render(request, 'cart.html')


def checkout(request):
    return render(request, 'checkout.html')



#USER:
def account(request):
    return render(request, 'user/account.html')


def login(request):
    return render(request, 'user/login.html')