from django.db import models

# Create your models here.
class Admin(models.Model):
    username = models.CharField(max_length=9, unique=True)
    password = models.CharField(max_length=20)
    is_boss = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class AdminPage(models.Model):
#     date = models.DateTimeField(auto_now=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.date)

class Reclama(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='Reclama')
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    time = models.TimeField(null=True)
    link = models.CharField(max_length=500, null=True)

    def formatted_time(self):
        return self.time.strftime('%H-%M') if self.time else ''


    def __str__(self):
        return str(self.time)






