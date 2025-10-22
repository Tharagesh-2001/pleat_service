# from rest_framework import serializers
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'phone']

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'phone']

#     def validate(self, data):
#         if CustomUser.objects.filter(email=data.get('email')).exists():
#             raise serializers.ValidationError({'email': 'This email is already registered.'})
#         if CustomUser.objects.filter(username=data.get('username')).exists():
#             raise serializers.ValidationError({'username': 'This username is already taken.'})
#         return data

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             phone=validated_data.get('phone', '')
#         )
#         return user



from rest_framework import serializers
from .models import CustomUser
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'profile_picture']
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None

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

class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

    def validate_phone(self, value):
        if not CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError('No user found with this phone number.')
        return value

class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(phone=data['phone'])
            if not user.otp or user.otp != data['otp'] or not user.is_otp_valid():
                raise serializers.ValidationError('Invalid or expired OTP.')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('No user found with this phone number.')
        return data