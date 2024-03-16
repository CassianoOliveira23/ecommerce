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
]