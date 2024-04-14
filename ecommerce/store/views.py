from django.shortcuts import render, redirect
from .models import *
from .utils import filter_products, price_min_max, order_products
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import uuid


def homepage(request):
    banners = Banner.objects.filter(active=True)
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def store(request, filter=None):
    products = Product.objects.filter(active=True)       
    products = filter_products(products, filter)
    if request.method == "POST":
        data = request.POST.dict()
        products = products.filter(price__gte=data.get("min_price"), price__lte=data.get("max_price"))
        
        if "size" in data:
            items = StokItem.objects.filter(product__in=products, size=data.get("size"))
            ids_products = items.values_list("product", flat=True).distinct()
            products = Product.objects.filter(id__in=ids_products)
        if "type" in data:
            products = products.filter(type__slug=data.get("type"))
        if "category" in data:
            products = products.filter(category__slug=data.get("category"))
        
    items = StokItem.objects.filter(quantity__gt=0, product__in=products)
    sizes = items.values_list("size", flat=True).distinct()
    ids_categories = products.values_list("category", flat=True).distinct()
    categories = ProductCategory.objects.filter(id__in= ids_categories)
    min, max = price_min_max(products)
    
    order = request.GET.get("order", "min-price")
    products = order_products(products, order)
    
    context = {"products": products, "min": min, "max": max, "sizes": sizes, "categories": categories}
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
    else:
        if  request.COOKIES.get("id_section"):
            id_section =  request.COOKIES.get("id_section")
            customer, created = Customer.objects.get_or_create(id_section=id_section)
        else:
            context = {"existent_customer": False, "order_items": None, "order": None}
            return render(request, 'cart.html', context)    
    order, created = Order.objects.get_or_create(customer=customer, done=False)
    order_items = OrderItem.objects.filter(order=order)
    context = {"order_items": order_items, "order": order, "existent_customer": True}
    return render(request, 'cart.html', context)



def addto_cart(request, id_product):
    if request.method == 'POST' and id_product:
        data = request.POST.dict()
        size = data.get("size")
        id_color = data.get("color")
        
        if not size or not id_color:
            return redirect('store')
        
        # taking customer
        response = redirect('cart')
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            if request.COOKIES.get("id_section"):
                id_section = request.COOKIES.get("id_section")
            else:
                id_section = str((uuid.uuid4))
                response.set_cookie(key="id_section", value=id_section, max_age=60*60*24*30)
            customer, created = Customer.objects.get_or_create(id_section=id_section)   
        order, created = Order.objects.get_or_create(customer=customer, done=False)
        stok_item = StokItem.objects.get(product__id=id_product, size=size, color__id=id_color)        
        order_items, created = OrderItem.objects.get_or_create(stok_item=stok_item, order=order)
        order_items.quantity += 1
        order_items.save()
        return response

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
            if  request.COOKIES.get("id_section"):
                id_section =  request.COOKIES.get("id_section")
                customer, created = Customer.objects.get_or_create(id_section=id_section)
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
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        if  request.COOKIES.get("id_section"):
            id_section =  request.COOKIES.get("id_section")
            customer, created = Customer.objects.get_or_create(id_section=id_section)
        else:
            return redirect('store')
    order, created = Order.objects.get_or_create(customer=customer, done=False)
    addresses = Address.objects.filter(customer=customer)
    context = {"order": order, "addresses": addresses}
    return render(request, 'checkout.html', context)


def checkout_order(request, id_order):
    if request.method == "POST":
        error = None
        data = request.POST.dict()
        total = data.get("total")
        order = Order.objects.get(id=id_order)
        if total != order.total_price:
            error = "price"
        if not "address" in data:
            error = "address"
        else:
            address = data.get("address")
            
        if not request.user.is_authenticated:
            email = data.get("email")
            try:
                validate_email(email)
            except ValidationError:
                error = "invalid_email"
            
        context = {"error": error}
        return redirect("checkout")
    else:
        return redirect("store")
    

def add_address(request):
    if request.method == "POST":
        #Send form
        if request.user.is_authenticated:
            customer = request.user.customer
        else:
            if  request.COOKIES.get("id_section"):
                id_section =  request.COOKIES.get("id_section")
                customer, created = Customer.objects.get_or_create(id_section=id_section)
            else:
                return redirect('store')
        data = request.POST.dict()
        address = Address.objects.create(customer=customer, street=data.get("street"),
                                         number=int(data.get("number")), state=data.get("state"),
                                         city=data.get("city"), cep=data.get("cep"), complement=data.get("complement"))
        address.save()
        return redirect("checkout")
    else:
        context = {}
        return render(request, 'add_address.html', context)



#USER:
@login_required
def account(request):
    error = None
    changed = False
    if request.method == 'POST':
        data = request.POST.dict()
        if 'current_password' in data:
            #user is changing his password
            current_password = data.get("current_password")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")
            if new_password == confirm_password:
                user = authenticate(request, username=request.user.email, password=current_password)
                if user:
                    #correct password
                    user.set_password(new_password)
                    user.save()
                    changed = True
                else:
                    error = 'incorrect_password'
            else:
                error = "imcompatible_passwords"
        elif 'email' in data:
            #changing personal information
            email = data.get("email")
            fone = data.get("fone")
            name = data.get("name")
            if email != request.user.email:
                users = User.objects.filter(email=email)
                if len(users) > 0:
                    error = "existing_email"
            if not error:
                customer = request.user.customer
                customer.email = email
                request.user.email = email
                request.user.username = email
                customer.name = name
                customer.fone = fone
                customer.save()
                request.user.save()
                changed = True 
        else:
            error = "invalid_form"
    context = {"error": error, "changed": changed}
    return render(request, 'user/account.html', context)



@login_required
def my_orders(request):
    customer = request.user.customer
    orders = Order.objects.filter(done=True, customer=customer).order_by("-complete_date")
    context = {"orders": orders}
    return render(request, 'user/my_orders.html', context)
    


def to_sign_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        data = request.POST.dict()
        if "email" in data and "password" in data:
            email = data.get("email")
            password = data.get("password")
            user = authenticate(request, username=email, password=password)
            
            #to sign in
            if user:
                login(request, user)
                return redirect('store')
            else:
                error = True
        else:
            error = True
    context = {"error": error}
    return render(request, 'user/login.html', context)
        

def create_account(request):
    error = None
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        data = request.POST.dict()
        if "email" in data and "password" in data and "password_comfirm" in data:
            # Creating  an Account:
            email = data.get("email")
            password = data.get("password")
            password_comfirm = data.get("password_comfirm")
            try:
                validate_email(email)
            except ValidationError:
                error = "invalid_email"
            if password == password_comfirm:
                user, created = User.objects.get_or_create(username=email, email=email)
                if not created:
                    error = "existing_user"
                else:
                    user.set_password(password)  
                    user.save() 
                    
                    #login user  
                    user = authenticate(request, username=email, password=password)
                    login(request, user)
                    
                    # if id_section in cookies:
                    if  request.COOKIES.get("id_section"):
                        id_section =  request.COOKIES.get("id_section")
                        customer, created = Customer.objects.get_or_create(id_section=id_section)
                    else:
                        #create customer
                        customer, created = Customer.objects.get_or_create(email=email)
                    customer.user = user
                    customer.email = email
                    customer.save()
                    return redirect('store')      
            else:
                error = "imcompatible_passwords"
        else:
            error = "to_fill"
    context = {"error": error}     
    return render(request, "user/create_account.html", context)


@login_required
def to_log_out(request):
    logout(request)
    return redirect('to_sign_in')
    
    
    
# TODO When a customer create an account in our website we have to create a customer for him
# TODO when you create an user account the username have to be equal to email 