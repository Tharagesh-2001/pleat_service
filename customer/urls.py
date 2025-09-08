from django.urls import path
from .views import RegisterView, LoginView, VerifyEmailView, CheckUsernameView

app_name = 'customer'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
]