from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.hashers import check_password
from .models import *

class PhoneSRL(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', )

class SendSmsSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()
    text = serializers.CharField(max_length=256)

class OtpSRL(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'otp')


class RegisterSRL(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'surname', 'fulname', "phone", "password")
        read_only_fields = ('password', 'phone')


class Log(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "password")



class Accaunt(serializers.ModelSerializer):

    class Meta:
        model=User
        fields="__all__"
        read_only_fields = ('password', 'phone')


class GetUserInfoSerializer(serializers.ModelSerializer):


    class Meta:
        model=User
        fields=('id','phone', 'name',  'image')
        read_only_fields = ('password',)


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'password2']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['password2']:
            raise serializers.ValidationError({'passwords': "The two password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.get('old_password')
        if not check_password(old_password, instance.password):
            raise serializers.ValidationError({'old_password': 'Wrong password'})
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance



class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ('phone', 'verify_code', 'step_change_phone')
        extra_kwargs = {
            'step_change_phone': {'read_only': True}
        }

    def update(self, instance, validated_data):
        verify_code = validated_data['verify_code']
        if instance.verify_code == verify_code:
            instance.is_verified = True
            if instance.step_reset == 'send':
                instance.step_reset = 'confirmed'
            if instance.step_change_phone:
                if instance.step_change_phone == 'send':
                    instance.step_change_phone = 'confirmed'
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'error': 'Phone number or verify code incorrect'})



class ResetPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('phone', 'new_password', 're_new_password')

    def validate(self, attrs):
        if not attrs['new_password']:
            raise serializers.ValidationError({'new_password': 'This field is required.'})

        if not attrs['re_new_password']:
            raise serializers.ValidationError({'re_new_password': 'This field is required.'})

        if attrs['new_password'] != attrs['re_new_password']:
            raise serializers.ValidationError({'passwords': "The two password fields didn't match."})

        return attrs

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"




