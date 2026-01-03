# for testing purpose
# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("HomePage")

from django.shortcuts import render
from store.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True) # to display all the products we added on our websie
    
    context = {"products":products,}
    
    return render(request, "home.html", context)