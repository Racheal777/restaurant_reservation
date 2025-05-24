
from .models import Restaurant, OpeningHour, Table
from django.db import transaction

class RestaurantRepository:
    
    
    @staticmethod
    def get_all_restaurants():
        """
        Retrieve all restaurants  with related data.
        """
        return Restaurant.objects.select_related('owner').prefetch_related('tables', 'opening_hours').only(
            'id', 'name', 'address', 'owner__id', 'owner__username'
        ).all()
    
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        """
        Retrieve a restaurant by its ID .
        """
        return Restaurant.objects.select_related('owner').prefetch_related('tables', 'opening_hours').only(
            'id', 'name', 'address', 'owner__id', 'owner__username'
        ).get(id=restaurant_id)
        
    @staticmethod
    def create_restaurant(serializer, user):
        validate_data = serializer.validated_data
        
        opening_hours_data = validate_data.pop('opening_hours', [])
        tables_data = validate_data.pop('tables', [])
        restaurant = Restaurant.objects.create(owner=user, **validate_data)
        
        for hour_data in opening_hours_data:
            OpeningHour.objects.create(restaurant=restaurant, **hour_data)
            
        for table_data in tables_data:
            Table.objects.create(restaurant=restaurant, **table_data)
        return restaurant
       
       
    @staticmethod
    def update_restaurant(restaurant_id, owner, data):
        """
        Update a restaurant's details.
        """
        with transaction.atomic():
            restaurant = Restaurant.objects.filter(id=restaurant_id).first()
            if not restaurant:
                return None
            
            
            
          
    
    
    @staticmethod
    def delete(instance):
        """
        Delete a restaurant instance.
        """
        instance.delete()
        return True
    
    