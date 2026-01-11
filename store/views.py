from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from carts.views import _cart_id
from carts.models import CartItem
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from.models import ReviewRating
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import OrderProduct

# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
        paginator =  Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) # page--> page=2 in url
        product_count = products.count() # to show  prodcut count on website

        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id") # to display all the products we added on our websie
        paginator =  Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) # page--> page=2 in url
        product_count = products.count() # to show  prodcut count on website

    
    context = { #"products":products,
                 "products": paged_products,
                 "product_count":product_count,}
    
    return render(request, "store/store.html", context)

# single product page
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug,
            slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=single_product
        ).exists()
    except Exception as msg:
        raise msg

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user,
                product_id=single_product.id
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # REMOVED DUPLICATE BLOCK (this caused the error)

    reviews = ReviewRating.objects.filter(
        product_id=single_product.id,
        status=True
    )

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews
    }
    return render(request, "store/product_detail.html", context)

# def product_detail(request, category_slug, product_slug):
#     try:
#         # to get access to slug attribite of category model
#         single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
#         # accessing cart modules cart_id is the fk of Cart so from CartItems'cart, we;re accessing cart_id whihc is FK of Cart method 
#         in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() 
#         # return HttpResponse(in_cart) # returns true or false for products in cart or not in cart
#         # exit()
#     except Exception as msg:
#         raise msg
    
#     if request.user.is_authenticated:
#         try:
#             orderproduct= OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
#         except OrderProduct.DoesNotExist:
#             orderproduct = None
#     else:
#         orderproduct = None
    
#     try:
#          orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
#     except OrderProduct.DoesNotExist:
#         orderproduct = None

#     # get all the reviews
#     reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

#     context = {
#         "single_product": single_product,
#         "in_cart": in_cart,
#         "orderproduct": orderproduct,
#         "reviews": reviews
#     }
#     return render(request, "store/product_detail.html", context)

def search(request):
    # return HttpResponse("Search Page")
    if "keyword" in request.GET:
        keyword=request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        "products" : products,
        "product_count": product_count,

    }
    return render(request, "store/store.html", context  )

from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import ReviewRating, Product
from .forms import ReviewForm

# def submit_review(request, product_id):
#     url = request.META.get('HTTP_REFERER')  # redirect back to the product page
#     product = get_object_or_404(Product, id=product_id)  # <-- fetch the product safely

#     if request.method == "POST":
#         try:
#             # Check if the user has already submitted a review for this product
#             reviews = ReviewRating.objects.get(user_id=request.user.id, product=product)
#             form = ReviewForm(request.POST, instance=reviews)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Thank you! Your review has been updated')
#                 return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = form.save(commit=False)
#                 data.product = product
#                 data.user = request.user
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.save()
#                 messages.success(request, 'Thank you! Your review has been submitted')
#                 return redirect(url)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ReviewRating, Product
from .forms import ReviewForm

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    url = request.META.get('HTTP_REFERER', '/')

    if request.method == "POST":
        # Try to get existing review
        review = ReviewRating.objects.filter(user=request.user, product=product).first()

        if review:
            # Update existing review
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your review has been updated.")
                return redirect(url)
        else:
            # Create new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.product = product
                data.user = request.user
                data.ip = request.META.get('REMOTE_ADDR')
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
