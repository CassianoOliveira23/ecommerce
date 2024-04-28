from django.urls import path
from django.contrib.auth import views
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
    path('completeorder/<int:id_order>/', complete_order, name="complete_order"),
    path('completepayment/', complete_payment, name="complete_payment"),
    path('approvedorder/<int:id_order>/', approved_order, name="approved_order"),
    
    path('account/', account, name="account"),
    path('myorders/', my_orders, name="my_orders"),
    path('login/', to_sign_in, name="to_sign_in"),
    path('createacount/', create_account, name="create_account"),
    path('logout/', to_log_out, name="to_log_out"),
    
    path('managestore/', manage_store, name="manage_store" ),
    path('exportreport/<str:report>/', export_report, name="export_report" ),
    
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
