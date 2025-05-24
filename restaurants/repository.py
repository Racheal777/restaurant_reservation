
from .models import Restaurant
from django.db import transaction

class RestaurantRepository:
    @staticmethod
    def get_all_restaurants():
        """
        Retrieve all restaurants from the database.
        """
        return Restaurant.objects.prefetch_related('tables', 'opening_hours').all()
    
    
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        """
        Retrieve a restaurant by its ID.
        """
        return Restaurant.objects.prefetch_related('tables', 'opening_hours').get(id=restaurant_id)
    
    @staticmethod
    def create_restaurant(data, owner):
        serializer = data
        restaurant = serializer.save(owner=owner)
        return restaurant
       
       
    @staticmethod
    def update_restaurant(restaurant_id, data):
        """
        Update a restaurant's details.
        """
        with transaction.atomic():
            restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            if restaurant:
                for key, value in data.items():
                    setattr(restaurant, key, value)
                restaurant.save()
                return restaurant
            return None
    
    
    @staticmethod
    def delete(instance):
        """
        Delete a restaurant instance.
        """
        instance.delete()
        return True
    
    