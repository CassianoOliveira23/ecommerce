from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    fone = models.CharField(max_length=200, null=True, blank=True)
    id_section = models.CharField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.email)
 

class ProductCategory(models.Model):
    name =  models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.name)


class ProductType(models.Model):
    name =  models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.name)


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey(ProductType, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Product: {self.name} | Category: {self.category} | Type: {self.type} | Price: {self.price}"
    
    def total_sales(self):
        items = OrderItem.objects.filter(order__done=True, stok_item__product=self.id)
        total = sum([items.quantity for items in items])
        return total

class Color(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.name)


class StokItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.product.name} | Size: {self.size} | Color: {self.color}"


class Address(models.Model):
    street = models.CharField(max_length=400, null=True, blank=True)
    number = models.IntegerField(default=0)
    complement = models.CharField(max_length=400, null=True, blank=True)
    postal_code = models.IntegerField(default=0)
    city = models.CharField(max_length=400, null=True, blank=True)
    state = models.CharField(max_length=400, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self) -> str:
        return f"{self.customer.email} - {self.street} - {self.city} - - {self.postal_code} - - {self.state}"

    
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    done = models.BooleanField(default=False)
    transaction_code = models.CharField(max_length=200, null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    complete_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Customer: {self.customer.email} | id_order: {self.id} | Done: {self.done}"
    
    @property
    def total_price(self):
        order_items = OrderItem.objects.filter(order__id=self.id)
        price = sum( [item.total_price for item in order_items])
        return price
    
    @property
    def total_quantity(self):
        order_items = OrderItem.objects.filter(order__id=self.id)
        quantity = sum( [item.quantity for item in order_items])
        return quantity
    
    @property
    def items(self):
        order_items = OrderItem.objects.filter(order__id=self.id)
        return order_items
    
    

class OrderItem(models.Model):
    stok_item = models.ForeignKey(StokItem, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"order_id: {self.order.id} | Product: {self.stok_item.product}, {self.stok_item.size}, {self.stok_item.color.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.stok_item.product.price
        
    

class Banner(models.Model):
    image = models.ImageField(null=True, blank=True)
    link = models.CharField(max_length=400, null=True, blank=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.link} - Active: {self.active}"   
    

class Payment(models.Model):
    id_payment = models.CharField(max_length=400)  
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    aprove = models.BooleanField(default=False) 
    

   