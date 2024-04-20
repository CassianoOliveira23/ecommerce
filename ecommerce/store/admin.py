from django.contrib import admin
from .models import *

# Register your models here:
admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(StokItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Banner)
admin.site.register(Color)
admin.site.register(Payment)

