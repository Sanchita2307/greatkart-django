# this function takes data as args and return dict
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)