from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProducInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class RecProSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecPro
        fields = "__all__"

