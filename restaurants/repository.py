
from .models import Restaurant, OpeningHour, Table
from django.db import transaction
from django.shortcuts import get_object_or_404

class RestaurantRepository:
    
    @staticmethod
    def get_all_restaurants():
        """
        Retrieve all restaurants  with related data.
        """
        return Restaurant.objects.select_related('owner')
        
        
    
    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        """
        Retrieve a restaurant by its ID .
        """
        
        return Restaurant.objects.filter(id=restaurant_id).select_related('owner').first()
        
        
        
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
            restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=owner)
            editable_fields = {f.name for f in Restaurant._meta.fields if f.name not in ['id', 'owner']}
            for field, value in data.items():
                if field in editable_fields:
                    setattr(restaurant, field, value)
            restaurant.save()
            return restaurant
           
            
            
            
          
    
    @staticmethod
    def delete(instance):
        """
        Delete a restaurant instance.
        """
        instance.delete()
        return True
    
    