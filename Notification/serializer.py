from rest_framework import serializers
from .models import *


class AdminNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationAdmin
        fields = "__all__"

        def to_representation(self, instance):
            representation = super(AdminNotificationsSerializer, self).to_representation(instance)
            representation['title'] = "Yangi xabar"
            representation['text'] = f"Sizda yangi xabar bor!"
            # representation['text'] = f"Sizda {instance.client_notify.translator.email} tomonidan xabar bor!"
            return representation


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationUser
        fields = "__all__"

        def to_representation(self, instance):
            representation = super(UserNotificationSerializer, self).to_representation(instance)
            representation['title'] = "Yangi xabar"
            representation['text'] = f"Sizda yangi xabar bor!"
            return representation


