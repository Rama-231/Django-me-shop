from django.shortcuts import render,redirect
from products.models import Product,Category
# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'home/home.html', context)


def search(request):
    query = request.GET['search']
    if query:
        search_products = Product.objects.filter(product_name__icontains=query )
        search_category = Category.objects.filter(category_name__icontains = query)

        if search_products:
            if search_category:
                search_category = Category.objects.get(category_name__icontains = query)
                product_obj = Product.objects.filter(category=search_category)

                search_result = search_products.union(product_obj)
                context = {'search_result':search_result,'query':query}
                return render(request, 'home/search.html' , context)

            else:
                return render(request, 'home/search.html' , {'search_result':search_products,'query':query})

        else:
            search_error= "Not found"
            return render(request, 'home/search.html' , {'search_error':search_error,'query':query})
    
    return redirect('home')

        
