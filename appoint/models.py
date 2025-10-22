# from django.db import models
# from customer.models import CustomUser
# from django.utils import timezone

# def get_current_date():
#     return timezone.now().date

# class Appoint(models.Model):
#     customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     date = models.DateField(default=get_current_date)  # Dynamic for future creates
    
#     # Status (if added)
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ]
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
#     # Other fields...
    
#     def __str__(self):
#         return f"{self.customer.username} - {self.date}"