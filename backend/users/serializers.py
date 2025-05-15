from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Subscription
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password", "avatar")
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_password(self, value):
        """Валидация пароля"""
        if len(value) < 8:
            raise serializers.ValidationError(
                'Пароль должен содержать не менее 8 символов'
            )
        return value
        
    def validate_username(self, value):
        """Валидация имени пользователя"""
        if len(value) < 3:
            raise serializers.ValidationError(
                'Имя пользователя должно содержать не менее 3 символов'
            )
        return value

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()
        return user


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "subscribed_to")