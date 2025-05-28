from .models import Restaurant, OpeningHour, Table
from django.db import transaction
from django.shortcuts import get_object_or_404

class RestaurantRepository:

    @staticmethod
    def get_all_restaurants():
        return Restaurant.objects.select_related('owner')

    @staticmethod
    def get_restaurant_by_id(restaurant_id):
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
        with transaction.atomic():
            restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=owner)
            editable_fields = {f.name for f in Restaurant._meta.fields if f.name not in ['id', 'owner', 'created_at']}
            for field, value in data.items():
                if field in editable_fields:
                    setattr(restaurant, field, value)
            restaurant.save()
            return restaurant

    @staticmethod
    def delete_restaurant(instance):
        instance.delete()
        return True

    @staticmethod
    def create_opening_hour(restaurant_id, owner, data):
        with transaction.atomic():
            restaurant = get_object_or_404(
                Restaurant,
                id=restaurant_id,
                owner=owner
            )
            new_opening_hour = OpeningHour(restaurant=restaurant, **data)
            new_opening_hour.save()
            return new_opening_hour

    @staticmethod
    def update_opening_hour(opening_hour_id, owner, data):
        with transaction.atomic():
            opening_hour = get_object_or_404(
                OpeningHour,
                id=opening_hour_id,
                restaurant__owner=owner
            )
            editable_fields = {
                f.name for f in OpeningHour._meta.fields
                if f.name not in ['id', 'restaurant']
            }
            for field, value in data.items():
                if field in editable_fields:
                    setattr(opening_hour, field, value)
            opening_hour.save()
            return opening_hour

    @staticmethod
    def delete_opening_hour(instance):
        instance.delete()
        return True

    @staticmethod
    def create_table(restaurant_id, owner, data):
        with transaction.atomic():
            restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=owner)
            new_table = Table(restaurant=restaurant, **data)
            new_table.save()
            return new_table

    @staticmethod
    def update_table(table_id, owner, data):
        with transaction.atomic():
            table = get_object_or_404(
                Table,
                id=table_id,
                restaurant__owner=owner
            )
            editable_fields = {
                f.name for f in Table._meta.fields
                if f.name not in ['id', 'restaurant']
            }
            for field, value in data.items():
                if field in editable_fields:
                    setattr(table, field, value)
            table.save()
            return table

    @staticmethod
    def delete_table(instance):
        instance.delete()
        return True
