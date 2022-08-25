from django.db import models
from django.contrib.auth.models import User
from Base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 
 
from products.models import Product,SizeVariant,Coupon 

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    
    profile_image = models.ImageField(upload_to="profile")

    


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete= models.CASCADE , related_name='carts')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL , null=True,blank=True)
    is_paid = models.BooleanField(default=False)

    def get_total_price(self):
        cart_items = self.cart_item.all()
        total_price=0
        for cart_item in cart_items:
            total_price = total_price + cart_item.get_product_price()
        return total_price

    def total_discount_price(self):
        if self.coupon:
            if self.get_total_price() > self.coupon.minnmum_amount:  
                return self.get_total_price() - self.coupon.discount_price
        return self.get_total_price()

    def get_discount_price(self):
        if self.coupon:
            return self.coupon.discount_price
        return 0

class CartItem(BaseModel):
    cart =models.ForeignKey(Cart, on_delete=models.CASCADE , related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True , blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete = models.SET_NULL, null=True,blank=True,)
    
    def get_product_price(self):
        price = self.product.price
        if self.size_variant:
            size_variant_price = self.size_variant.price
            return price+size_variant_price
        return price


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="address")
    address_name = models.TextField()
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + self.user.last_name
    