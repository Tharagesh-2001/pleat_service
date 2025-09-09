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
from django.templatetags.static import static

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'profile_picture']
    
    def get_profile_picture(self, obj):
        # If the user has a profile picture, return the full URL
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                # Use request.build_absolute_uri for full URL
                return request.build_absolute_uri(obj.profile_picture.url)
            else:
                # Fallback to relative URL
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