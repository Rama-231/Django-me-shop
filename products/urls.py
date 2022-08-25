from products.views import *
from django.urls import path,include

urlpatterns = [
    path('<slug>/', get_product , name="get_product"),
]