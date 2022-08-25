from django.shortcuts import render
from products.models import Product
from accounts.models import Cart , CartItem
# Create your views here.

def get_product(request ,slug):
    try:
        product = Product.objects.get(slug = slug)
        check = False
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
            
            if cart:
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.filter(cart=cart)
                
                if cart_item:
                    for i in cart_item:
                        if product.uid == i.product.uid:
                            check = True
        context = {'product': product,'check':check}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.product_price_by_size(size)
            context['selected_size']= size
            context['updated_price'] = price

        return render(request, 'product/product.html', context = context)

    except Exception as e:
        print(e)