from rest_framework import serializers
from .models import *
from User.models import Order

class AdminLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"

class GetOrderSerializer():
    class Meta:
        pass



class EditorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('state', )


class ReclamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclama
        fields = "__all__"












