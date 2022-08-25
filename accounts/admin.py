from django.contrib import admin
from .models import Profile,Cart,CartItem,Address
# Register your models here.

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
