from django.db import models
from Admin.models import Admin

# Create your models here.
class Product(models.Model):
    categ = (
        ('Elektronika', 'Elektronika'),
        ('Maishiy_texnika', 'Maishiy_texnika'),
        ('Noutbooklar', 'Noutbooklar'),
        ('Smartfonlar', 'Smartfonlar'),
        ('Planshetlar', 'Planshetlar')
    )
    name = models.CharField(max_length=250, null=True)
    about = models.TextField(null=True)
    quantity = models.IntegerField(null=True)
    cost = models.IntegerField(null=True)
    category = models.CharField(max_length=250, choices=categ, null=True)
    color = models.CharField(max_length=13, null=True)
    image = models.ImageField(upload_to = 'rasmlar/', null=True)
    time = models.DateTimeField(auto_now=True)
    prosent = models.IntegerField(null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


