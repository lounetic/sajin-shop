from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)

class Province(models.Model):
    title = models.CharField(max_length=100, unique=True)

class City(models.Model): # فارن کی مربوط به جدولی هست که فقط یکی ازش موجوده / یک ارتباط داره (مثل استان)
    title = models.CharField(max_length=100)
    province = models.ForeignKey(Province,on_delete=models.CASCADE)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    recipient_firstname = models.CharField(max_length=100, null=True, blank=True)
    recipient_lastname = models.CharField(max_length=100, null=True, blank=True)
    recipient_phone = models.CharField(max_length=11, null=True, blank=True)
    city = models.ForeignKey(City, on_delete= models.SET_NULL, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    unit = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(max_length=255, null=True,blank=True)
    def __str__(self):
        return self.address

