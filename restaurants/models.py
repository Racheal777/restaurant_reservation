from django.db import models
from django.conf import settings

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class OpeningHour(models.Model):
    DAYS = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='opening_hours')
    day = models.CharField(max_length=3, choices=DAYS)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_closed = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.day} ({self.open_time} - {self.close_time})"
    
    
class Table(models.Model):
        restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
        table_number = models.CharField(max_length=10)
        capacity = models.PositiveIntegerField()
        is_outdoor = models.BooleanField(default=False)
        is_available = models.BooleanField(default=True)
        
        def __str__(self):
            return f"Table {self.table_number} ({self.capacity} seats) at {self.restaurant.name}"
