from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.models import User
from accounts.models import *
from products.models import Product,SizeVariant
from django.http import HttpResponseRedirect
# Create your views here.




def login_view(request):
   
        
        if request.method =='POST' :   
            email = request.POST['loginemail']
            password = request.POST['loginpassword']

            user = authenticate(username = email , password = password)
            if  user:
                login(request,user)
                messages.success(request, 'Successfully logged in.')
                return redirect('home')

            else:
                messages.warning(request, 'User not found.')    
                return redirect('login')
            
        return render(request, 'accounts/login.html')

    



def register(request):

    if request.method=='POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = User.objects.filter(email=email)
        if not user:
            if cpassword==password:
                user = User.objects.create(first_name=firstname,last_name=lastname,email=email,username=email,password=password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registered successfully.')
                return redirect('register')
            else:
                messages.warning(request, 'Please check your confirm password. ')
                return redirect('register')

        messages.warning(request, 'User already exist.')
        return redirect('register')
    return render(request, 'accounts/register.html')



def logout_view(request):
    logout(request)
    return redirect('home')





def add_to_cart(request,uid):
    if request.user.is_authenticated:
        variant = request.GET.get('variant')
        product = Product.objects.get(uid=uid)
        user = request.user
        cart , _ = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.create(cart=cart,product=product)
        if variant:
            size_variant = SizeVariant.objects.get(size_name=variant)
            cart_item.size_variant = size_variant
            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))   

    else:
        return redirect('login')





def remove_cart(request , cart_item_id):
    try:
        cart_item = CartItem.objects.get(uid = cart_item_id)
        cart_item.delete()
    except Exception as e:
        print(e)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))







def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cart_item = ""
        if cart:
            cart = Cart.objects.get(user=request.user)
            cart_item =CartItem.objects.filter(cart=cart)
        
        context = {'cart_items':cart_item,'cart':cart}
        if request.method=='POST':
            
            coupon = request.POST['coupon']
            coupon_obj = Coupon.objects.filter(coupon_code=coupon)

            if not coupon_obj:
                messages.warning(request, 'Invalid coupon.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            coupon_obj = Coupon.objects.get(coupon_code=coupon)

            if cart.coupon == coupon_obj:
                messages.warning(request, 'Coupon already applied.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


            if coupon_obj.is_expired:
                messages.warning(request, 'Coupon Expired.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            if cart.get_total_price() < coupon_obj.minnmum_amount:
                messages.warning(request, f'Amount should be greater than {coupon_obj.minnmum_amount}.')
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


            cart.coupon = coupon_obj
            cart.save()
            
            messages.success(request, 'Coupon applied.')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) 

        
        
        return render(request, 'accounts/cart.html',context)

    else:
        return redirect('login')







def remove_coupon(request , cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon removed.')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))







def address (request ):

    address_user = Address.objects.filter(user=request.user)

    if address_user:
        address_user = Address.objects.get(user=request.user)
        if request.method == 'POST':
            address_user.address_name = request.POST['address']
            address_user.city = request.POST['city']
            address_user.zipcode = request.POST['zipcode']
            address_user.state = request.POST['state']
            address_user.country = request.POST['country']
            
        
            address_user.save()

            



    else:
        if request.method == 'POST':
            address_name = request.POST['address']
            city = request.POST['city']
            zipcode = request.POST['zipcode']
            state = request.POST['state']
            country = request.POST['country']
            user = request.user
            address_obj = Address.objects.create(user=user,address_name=address_name,city=city,zipcode=zipcode,state=state,country=country)
            address_obj.save()
            return render(request, 'accounts/address.html',{'address_user':address_user} )


    return render(request, 'accounts/address.html' , {'address_user':address_user})








def order(request , product_uid ):
    if request.user.is_authenticated:
        product_item = Product.objects.get(uid=product_uid)
        address_user = Address.objects.filter(user=request.user)
        if address_user:
            address_user = Address.objects.get(user=request.user)
        return render(request, 'accounts/order.html',{'product_item':product_item , 'address_user':address_user})
    
    else:
        return redirect('login')

   



def confirm_order(request):
    return render(request,'accounts\confirmorder.html')