from django.db import models
from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    class Meta:
        db_table = "cart"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True) # many products can have same variation
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    ## gives error
    # def __str__(self):
    #     return self.product

    # def __unicode__(self):
    #     return self.product

    def __str__(self):
        return self.product.product_name    


