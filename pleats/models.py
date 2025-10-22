# from django.db import models
# from customer.models import CustomUser
# from django.utils import timezone

# def get_current_date():
#     return timezone.now().date

# class Appointment(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     service = models.CharField(max_length=50)
#     date = models.DateField()
#     time = models.CharField(max_length=10)
#     address = models.TextField(blank=True)
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.service} on {self.date}"
    
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



from django.db import models
from customer.models import CustomUser
from django.utils import timezone

def get_current_date():
    return timezone.now().date()

class Appointment(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    service = models.CharField(max_length=50)
    date = models.DateField(default=get_current_date)
    time = models.CharField(max_length=10)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        if self.customer:
            customer_name = self.customer.username
        else:
            customer_name = self.name or "Unknown Customer"
        return f"{customer_name} - {self.service} on {self.date}"