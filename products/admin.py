from django.contrib import admin
from products.models import *
# Register your models here.

admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin ):
    
    inlines = [ProductImageAdmin]

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    model = SizeVariant

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    model = ColorVariant


admin.site.register(Product , ProductAdmin)
admin.site.register(ProductImage)

admin.site.register(Coupon)
