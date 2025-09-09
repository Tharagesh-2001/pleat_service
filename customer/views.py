# import uuid
# from django.core.mail import send_mail
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import RegisterSerializer, UserSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.urls import reverse
# from django.contrib.auth import authenticate, update_session_auth_hash
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.conf import settings
# from .models import CustomUser
# from rest_framework.permissions import IsAuthenticated
# # from google.oauth2 import id_token
# # from google.auth.transport import requests

# @method_decorator(csrf_exempt, name='dispatch')
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             verification_token = str(uuid.uuid4())
#             user.verification_token = verification_token
#             user.save()

#             verification_link = request.build_absolute_uri(
#                 reverse('customer:verify-email', kwargs={'token': verification_token})
#             )

#             # send_mail(
#             #     'Verify Your Email',
#             #     f'Please verify your email by clicking this link: {verification_link}',
#             #     settings.EMAIL_HOST_USER,
#             #     [user.email],
#             #     fail_silently=False,
#             try:
#                 send_mail(
#                     'Verify Your Email',
#                     f'Please verify your email by clicking this link: {verification_link}',
#                     settings.EMAIL_HOST_USER,
#                     [user.email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 # Log the error but proceed (optional: return a warning to the user)
#                 print(f"Email sending failed: {e}")

#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'phone': user.phone
#                 },
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh),
#                 'message': 'Registration successful. Please check your email to verify your account.'
#             }, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='dispatch')
# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         user = authenticate(request, email=email, password=password)  # Use the custom backend
#         if user:
#             if not user.is_verified:
#                 return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_401_UNAUTHORIZED)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'phone': user.phone
#                 },
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# @method_decorator(csrf_exempt, name='dispatch')
# class VerifyEmailView(APIView):
#     def get(self, request, token):
#         try:
#             user = CustomUser.objects.get(verification_token=token)
#             user.is_verified = True
#             user.verification_token = None  # Clear token after verification
#             user.save()
#             return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'Invalid or expired verification link.'}, status=status.HTTP_400_BAD_REQUEST)
        
# @method_decorator(csrf_exempt, name='dispatch')
# class CheckUsernameView(APIView):
#     def get(self, request):
#         username = request.query_params.get('username', '')
#         if not username:
#             return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
#         if CustomUser.objects.filter(username=username).exists():
#             return Response({'available': False, 'message': 'This username is already taken.'}, status=status.HTTP_200_OK)
#         return Response({'available': True, 'message': 'This username is available.'}, status=status.HTTP_200_OK)
        
# @method_decorator(csrf_exempt, name='dispatch')
# class CurrentUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    
# class ChangePasswordView(APIView):
#     permission_classes = [IsAuthenticated]

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request):
#         old_password = request.data.get('old_password')
#         new_password = request.data.get('new_password')
#         user = request.user

#         if not user.check_password(old_password):
#             return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
#         if not new_password:
#             return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

#         user.set_password(new_password)
#         user.save()
#         update_session_auth_hash(request, user)  # Update session to prevent logout
#         return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


import uuid
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import authenticate, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            verification_token = str(uuid.uuid4())
            user.verification_token = verification_token
            user.save()

            verification_link = request.build_absolute_uri(
                reverse('customer:verify-email', kwargs={'token': verification_token})
            )

            try:
                send_mail(
                    'Verify Your Email',
                    f'Please verify your email by clicking this link: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")

            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': 'Registration successful. Please check your email to verify your account.'
            }, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user:
            if not user.is_verified:
                return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
            user.is_verified = True
            user.verification_token = None
            user.save()
            return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid or expired verification link.'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class CheckUsernameView(APIView):
    def get(self, request):
        username = request.query_params.get('username', '')
        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'available': False, 'message': 'This username is already taken.'}, status=status.HTTP_200_OK)
        return Response({'available': True, 'message': 'This username is available.'}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = request.user

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Update session to prevent logout
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        user = request.user
        if 'profile_picture' not in request.FILES:
            return Response({'error': 'No profile picture uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        profile_picture = request.FILES['profile_picture']
        user.profile_picture = profile_picture
        user.save()

        # Return the full URL
        request_full_path = request.build_absolute_uri()
        profile_picture_url = user.profile_picture.url
        if not profile_picture_url.startswith('http'):
            profile_picture_url = request.build_absolute_uri(profile_picture_url)

        serializer = UserSerializer(user, context={'request': request})
        return Response({
            'message': 'Profile picture updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)