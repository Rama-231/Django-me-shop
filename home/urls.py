from home.views import *
from django.urls import path


urlpatterns = [
    path('',home , name="home"),
    path('search/' , search ,name="search"),
]