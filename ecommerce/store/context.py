from .models import Order, OrderItem

def cart(request):
    items_cart = 0
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        print("Logged out")
    
    order, created = Order.objects.get_or_create(customer=customer, done=False)
    order_items = OrderItem.objects.filter(order=order)
    for item in order_items:
        items_cart += item.quantity
   
    return{"itens_cart": items_cart }


# TODO When a customer create an account in our website we have to create a customer for him