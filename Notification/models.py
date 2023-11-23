from django.db import models
from User.models import User, Order
from Admin.models import Admin
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
@receiver(signal=post_save, sender=Order)
def attach_notification_to_translator(sender, **kwargs):
    order = kwargs['instance']
    if order.file_order is not None:
        NotificationUser.objects.create(user=order.translator, client_order=order)


class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"(User_Notification ID : {self.id}) | Is_Read:{self.is_read} | For {self.user}"

    class Meta:
        ordering = ['id']
        verbose_name = 'User Notification'
        verbose_name_plural = 'User Notifications'



@receiver(signal=post_save, sender=Order)
def attach_notification_to_translator(sender, **kwargs):
    order = kwargs['instance']
    if order.file_order is not None:
        NotificationAdmin.objects.create(user=order.translator, client_order=order)


class NotificationAdmin(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='Admin_n', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='Admin_n', null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"(Admin_Notification ID : {self.id}) | Is_Read:{self.is_read} | For {self.user}"

    class Meta:
        ordering = ['id']
        verbose_name = 'Admin Notification'
        verbose_name_plural = 'Admin Notifications'























