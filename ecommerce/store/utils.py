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
    