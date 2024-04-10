from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name="homepage"), 
    path('store/', store, name="store"),
    path('store/<str:filter>/', store, name="store"),
    path('product/<int:id_product>/', see_product, name="see_product"),
    path('product/<int:id_product>/<int:id_color>/', see_product, name="see_product"),
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('addtocart/<int:id_product>/', addto_cart, name="addto_cart"),
    path('removecart/<int:id_product>/', remove_cart, name="remove_cart"),
    path('addaddress/', add_address, name="add_address"),
    path('account/', account, name="account"),
    path('login/', to_sign_in, name="to_sign_in"),
    path('createacount/', create_account, name="create_account"),
    path('logout/', to_log_out, name="to_log_out"),
]