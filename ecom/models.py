from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.FloatField(default=0.99)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title


class ProductInCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return float(format(self.product.price*self.quantity, '.3f'))

    def add_to_cart(self):
        self.quantity += 1
        self.product.quantity -= 1
        self.product.save()

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    costumer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    total_price = models.IntegerField()
    products = models.ManyToManyField(ProductInCart)


