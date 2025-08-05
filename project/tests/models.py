from django.db import models
from django.conf import settings
from account.models import Address
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Size(models.Model):
    size = models.CharField(max_length=10)
    def __str__(self):
        return self.size

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete= models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(max_length=2048)
    main_image = models.ImageField(upload_to='image/products', null=True)
    image1 = models.ImageField(upload_to='image/products', null=True,blank=True)
    image2 = models.ImageField(upload_to='image/products', null=True,blank=True)
    image3 = models.ImageField(upload_to='image/products', null=True,blank=True)
    sizes = models.ManyToManyField(Size, null=True, blank=True)
    def __str__(self):
        return self.title

class Cart(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete= models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.IntegerField()
    status = models.BooleanField(null=True)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product =models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()

# class Image(models.Model):
#     image = models.ImageField(upload_to='image/products')
#     product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True, blank=True)
