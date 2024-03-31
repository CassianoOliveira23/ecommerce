from .models import Order, OrderItem, Customer, ProductCategory, ProductType

def cart(request):
    items_cart = 0
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        if  request.COOKIES.get("id_section"):
            id_section =  request.COOKIES.get("id_section")
            customer, created = Customer.objects.get_or_create(id_section=id_section)
        else:    
            return{"items_cart": items_cart }
    
    order, created = Order.objects.get_or_create(customer=customer, done=False)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        items_cart += item.quantity
   
    return{"items_cart": items_cart }


def category_types(request):
    categories = ProductCategory.objects.all()
    types = ProductType.objects.all()
    return {"categories": categories, "types": types}


# TODO When a customer create an account in our website we have to create a customer for him