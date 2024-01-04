from rest_framework import serializers
from .models import *

class PaymentSRL(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"