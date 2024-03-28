from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name="homepage"), 
    path('store/', store, name="store"),
    path('store/<str:category_name>/', store, name="store"),
    path('product/<int:id_product>/', see_product, name="see_product"),
    path('product/<int:id_product>/<int:id_color>/', see_product, name="see_product"),
    path('account/', account, name="account"),
    path('login/', login, name="login"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('addtocart/<int:id_product>/', addto_cart, name="addto_cart"),
    path('removecart/<int:id_product>/', remove_cart, name="remove_cart"),
]