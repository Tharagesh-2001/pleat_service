import uuid
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import CustomUser
# from google.oauth2 import id_token
# from google.auth.transport import requests

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

            # send_mail(
            #     'Verify Your Email',
            #     f'Please verify your email by clicking this link: {verification_link}',
            #     settings.EMAIL_HOST_USER,
            #     [user.email],
            #     fail_silently=False,
            try:
                send_mail(
                    'Verify Your Email',
                    f'Please verify your email by clicking this link: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but proceed (optional: return a warning to the user)
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
        
        user = authenticate(request, email=email, password=password)  # Use the custom backend
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
            user.verification_token = None  # Clear token after verification
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
        
# class GoogleRegisterView(APIView):
#        def post(self, request):
#            token = request.data.get('token')
#            try:
#                id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
#                email = id_info['email']
#                username = id_info.get('name', email.split('@')[0])

#                user, created = CustomUser.objects.get_or_create(
#                    email=email,
#                    defaults={'username': username, 'is_verified': True}
#                )
#                if created:
#                    refresh = RefreshToken.for_user(user)
#                    return Response({
#                        'user': {'id': user.id, 'username': user.username, 'email': user.email},
#                        'access': str(refresh.access_token),
#                        'refresh': str(refresh)
#                    }, status=status.HTTP_201_CREATED)
#                refresh = RefreshToken.for_user(user)
#                return Response({
#                    'user': {'id': user.id, 'username': user.username, 'email': user.email},
#                    'access': str(refresh.access_token),
#                    'refresh': str(refresh)
#                }, status=status.HTTP_200_OK)
#            except ValueError:
#                return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)

# class GoogleLoginView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         try:
#             id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
#             email = id_info['email']
#             user = CustomUser.objects.get(email=email)
#             if not user.is_verified:
#                 return Response({'error': 'Please verify your email.'}, status=status.HTTP_401_UNAUTHORIZED)
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'user': {'id': user.id, 'username': user.username, 'email': user.email},
#                 'access': str(refresh.access_token),
#                 'refresh': str(refresh)
#             }, status=status.HTTP_200_OK)
#         except (ValueError, CustomUser.DoesNotExist):
#             return Response({'error': 'Invalid Google token or user not found'}, status=status.HTTP_400_BAD_REQUEST)