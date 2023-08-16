from enum import Enum
from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Options(Enum):
    OPTION_ONE = 'Cancelled'
    OPTION_TWO = 'Pending'
    OPTION_THREE = 'Closed'
    
class MyUser(AbstractUser):
    phone_number = models.IntegerField(default=0, null=True)
    address = models.CharField(max_length=100, null=True)   

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)     
    def __str__(self):
        return f"{self.name}"
    
class Product(models.Model):
    name = models.CharField(max_length=100, null=True)   
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0) 
    image = models.ImageField(upload_to="shop_images", null=True)    
    def __str__(self):
        return f"{self.name} - {self.category} - {self.price} - {self.stock} - {self.image}"
    
class PurchaseCard(models.Model):
    date = models.DateTimeField(null=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    status = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in Options])  
    def __str__(self):
        return f"{self.id} - {self.customer} - {self.status}"  
    
class PurchaseLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)    
    amount = models.IntegerField(default=0)
    purchase = models.ForeignKey(PurchaseCard, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.id} - {self.purchase} - {self.product} - {self.amount}"  


    