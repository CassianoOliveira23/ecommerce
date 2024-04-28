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
    categories_navbar = ProductCategory.objects.all()
    types_navbar = ProductType.objects.all()
    return {"categories_navbar": categories_navbar, "types_navbar": types_navbar}


def in_the_team(request):
    team = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name="team").exists():
            team = True
    return {"team": team}
            


