from django.urls import path,include
from accounts.views import *

urlpatterns = [
    path("login/",login_view , name ="login"),
    
    path('logout/', logout_view , name = "logout"),
    path("register/",register , name ="register"),
    path('add-to-cart/<uid>/',add_to_cart , name="add_to_cart"),
    path('cart/',cart,name="cart"),
    path('remove-item/<cart_item_id>/', remove_cart , name="remove_item"),
    path('remove-coupon/<cart_id>/', remove_coupon , name="remove_coupon"),
    path('address/', address , name="address"),


    path('order/<product_uid>/', order , name="order"),
    path('confirmorder/', confirm_order , name="confirmorder"),


]