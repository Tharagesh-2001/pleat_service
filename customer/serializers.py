from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone']

    def validate(self, data):
        if CustomUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({'email': 'This email is already registered.'})
        if CustomUser.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', '')
        )
        return user