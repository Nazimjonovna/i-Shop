from django.db import models

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
    rat = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )
    rate = models.CharField(max_length=10, choices=rat, default=1, null=True)
    pro = (
        ('is_buy', 'is_buy'),
        ('is_like', 'is_like')
    )
    pro_x = models.CharField(max_length=50, choices=pro, null=True)


    def __str__(self):
        return self.name


