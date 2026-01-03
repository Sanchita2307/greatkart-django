from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
        product_count = products.count()
    else:

        products = Product.objects.all().filter(is_available=True) # to display all the products we added on our websie
        product_count = products.count() # to show  prodcut count on website 
    
    context = {"products":products,
                   "product_count":product_count,}
    
    return render(request, "store/store.html", context)

# single product page
def product_detail(request, category_slug, product_slug):
    try:
        # to get access to slug attribite of category model
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as msg:
        raise msg
    
    context = {
        "single_product": single_product,
    }
    return render(request, "store/product_detail.html", context)

