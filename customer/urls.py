from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, CheckUsernameView, CurrentUserView, ChangePasswordView, UpdateProfilePictureView

app_name = 'customer'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-profile-picture/', UpdateProfilePictureView.as_view(), name='update-profile-picture'),
]