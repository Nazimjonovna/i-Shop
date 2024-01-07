from django.db import models
from Admin.models import Admin

# Create your models here.
class Product(models.Model):
    quantity = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now=True)
    prosent = models.IntegerField(null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    tasdiq = models.BooleanField(default=False)


    def __str__(self):
        return str(self.cost)



class ProductInfo(models.Model):
    categ = (
        ('Elektronika', 'Elektronika'),
        ('Maishiy_texnika', 'Maishiy_texnika'),
        ('Noutbooklar', 'Noutbooklar'),
        ('Smartfonlar', 'Smartfonlar'),
        ('Planshetlar', 'Planshetlar')
    )
    name = models.CharField(max_length=250, null=True)
    about = models.TextField(null=True)
    category = models.CharField(max_length=250, choices=categ, null=True)
    model = models.CharField(max_length = 250, null = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class Image(models.Model):
    image = models.ImageField(upload_to = 'rasmlar/', null=True)
    pro_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=13, null=True)

class RecPro(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'rec_pro')
    is_rec = models.BooleanField(default=True)


    def __str__(self):
        return str(self.is_rec)

