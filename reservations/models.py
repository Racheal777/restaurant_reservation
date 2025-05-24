from django.db import models
from django.conf import settings    



# Create your models here.

class Reservation(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey('restaurants.Table', on_delete=models.CASCADE, related_name='reservations')
    reservation_time = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-reservation_time']
        unique_together = ('table',  'reservation_time')
