from django.db import models
from User.models import Order
from Product.models import Product

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=9, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class AdminPage(models.Model):
    date = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)



