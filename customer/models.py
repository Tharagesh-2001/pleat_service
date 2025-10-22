from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=36, blank=True, null=True)  # UUID length is 36 characters
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # Store OTP
    otp_expiry = models.DateTimeField(blank=True, null=True)  # OTP expiry time

    def __str__(self):
        return self.username

    def is_otp_valid(self):
        """Check if OTP is valid and not expired."""
        if self.otp and self.otp_expiry:
            return timezone.now() <= self.otp_expiry
        return False