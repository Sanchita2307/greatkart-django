from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descrpition = models.TextField(max_length=255, blank=True) # optional                   
    cat_image = models.ImageField(upload_to="photos/categories/", blank=True) # potional and goes to defined folder

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        db_table = "Category"

    def get_url(self):
            return reverse("products_by_category", args= [self.slug]) #products_by_category comes from store mdeols.py

    def __str__(self):
        return self.category_name

