from django.db.models import Max, Min

def filter_products(products, filter):
    if filter:
        if "-" in filter:
            category, type = filter.split("-")
            products = products.filter(type__slug=type, category__slug=category)
        else:
            products = products.filter(category__slug=filter)
    return products


def price_min_max(products):
    min = 0
    max = 0
    if len(products) > 0:
        max = list(products.aggregate(Max("price")).values())[0]
        max = round(max, 2)
        
        min = list(products.aggregate(Min("price")).values())[0]
        min = round(min, 2)
    return min, max
    
def order_products(products, order):
    if order == "min-price":
        products = products.order_by("price")
    elif order == "max-price":
        products = products.order_by("-price")
    elif order == "best-sellers":
        product_list = []
        for product in products:
            product_list.append((product.total_sales(), product))
            product_list = sorted(product_list, reverse=True)
            products = [items[1] for items in product_list]
    return products