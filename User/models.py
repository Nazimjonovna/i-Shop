from django.db import models
from django.core.validators import RegexValidator
from Product.models import Product

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=255, null =True)
    surname = models.CharField(max_length=255, null =True)
    fulname = models.CharField(max_length=255, null =True) # ochestvo
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +998XXXXXXXXX kabi kiriting!")
    phone = models.CharField(validators=[phone_regex], max_length=9, unique=True)
    password = models.CharField(max_length=20, null =True)
    otp = models.CharField(max_length=4, null=True)
    idp = models.CharField(max_length=9, null=True) # bank schot kredit bo'lsa generatsiya qilish
    seria = models.CharField(max_length=2, null=True)
    raqam = models.CharField(max_length=7, null=True)
    pasport = models.FileField(upload_to = 'pasports/', null=True, blank=True)
    image = models.FileField(upload_to='image/', null=True, blank=True)
    card = models.CharField(max_length=4, null=True, blank=True) # amal qilish vaqti
    card_number = models.CharField(max_length=20, null=True, blank=True)
    vil = (
        ('Toshkent', 'Toshkent'),
        ('Navoiy', 'Navoiy'),
        ('Buxoro', 'Buxoro')
    )
    address = models.TextField()
    viloyat = models.CharField(max_length=30, choices=vil, default='Toshkent', null=True, blank=True)


    def __str__(self):
        return self.name


class ValidatedOtp(models.Model):
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +9989XXXXXXXX kabi kiriting!")
    phone = models.CharField(validators=[phone_regex],max_length=9,unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Kodni kiritishlar soni:')
    validated = models.BooleanField(default=False, help_text="Shaxsiy kabinetingizni yaratishingiz mumkin!")

    def __str__(self):
        return str(self.phone)


class Verification(models.Model):
    STATUS = (
        ('send', 'send'),
        ('confirmed', 'confirmed'),
    )
    phone = models.CharField(max_length=9, unique=True)
    verify_code = models.SmallIntegerField()
    is_verified = models.BooleanField(default=False)
    step_reset = models.CharField(max_length=10, null=True, blank=True, choices=STATUS)
    step_change_phone = models.CharField(max_length=30, null=True, blank=True, choices=STATUS)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} --- {self.verify_code}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    stat = (
        ('buyurtma_berish', 'buyurtma_berish'),
        ('buyurtma_tayyorlanmoqda', 'buyurtma_tayyorlanmoqda'),
        ('yetkazib_berish_jarayoni', 'yetkazib_berish_jarayoni'),
        ('yetkazilgan', 'yetkazilgan'),
        ('bekor_qilingan', 'bekor_qilingan')
    )
    state = models.CharField(max_length=200, choices=stat, default='buyurtma_berish')
    pay = (
        ('naqt', 'naqt'),
        ('card', 'card'),
        ('credit', 'credit')
    )
    payment = models.CharField(max_length=100, choices=pay, default='naqt')
    quantity = models.IntegerField(null=True)
    rat = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    rate = models.CharField(max_length=10, choices=rat, default=1, null=True)
    pro = (
        ('is_buy', 'is_buy'),
        ('is_like', 'is_like')
    )
    pro_x = models.CharField(max_length=50, choices=pro, null=True)
    oy = (
        ('6', '6'),
        ('12', '12'),
        ('24', '24')
    )
    oy_cre = models.CharField(max_length=50, choices=oy, default='6', null=True)
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +998XXXXXXXXX kabi kiriting!")
    phone_cre = models.CharField(validators=[phone_regex], max_length=9, unique=True, null=True)
    tasdiq = models.BooleanField(null=True)

    def __str__(self):
        return str(self.time)






















