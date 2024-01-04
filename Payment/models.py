from django.db import models
from User.models import *

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    st = (
        ('naqt', 'naqt'),
        ('credit', 'credit')
    )
    status = models.CharField(max_length=20, choices=st)

