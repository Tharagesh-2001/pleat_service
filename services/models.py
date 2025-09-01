from django.db import models

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('traditional', 'Traditional'),
        ('premium', 'Premium'),
        ('express', 'Express'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="services/")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="traditional")

    # For features list
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
