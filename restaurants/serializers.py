from .models import Restaurant, OpeningHour, Table
from rest_framework import serializers



class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = [ 'table_number', 'capacity', 'is_outdoor', 'is_available']
        read_only_fields = ['id', 'restaurant']
        

class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = [ 'day', 'open_time', 'close_time']
        read_only_fields = ['id', 'restaurant']
    
    def validate(self, data):
        if data['open_time'] >= data['close_time']:
            raise serializers.ValidationError("Open time must be before close time.")
        return data
    
    
class RestaurantSerializer(serializers.ModelSerializer):
    opening_hours = OpeningHourSerializer(many=True)
    tables = TableSerializer(many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'owner', 'created_at', 'opening_hours', 'tables']
        read_only_fields = ['id', 'owner', 'created_at']
        
    def create(self, validated_data):
            opening_hours_data = validated_data.pop('opening_hours')
            tables_data = validated_data.pop('tables')
            restaurant = Restaurant.objects.create(**validated_data)
            
            for hour_data in opening_hours_data:
                OpeningHour.objects.create(restaurant=restaurant, **hour_data)
                
            for table_data in tables_data:
                Table.objects.create(restaurant=restaurant, **table_data)
                
            return restaurant 
        
        
    def update(self, instance, validated_data):
        opening_hours_data = validated_data.pop('opening_hours', None)
        tables_data = validated_data.pop('tables', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if opening_hours_data is not None:
            instance.opening_hours.all().delete()
            for hour_data in opening_hours_data:
                OpeningHour.objects.create(restaurant=instance, **hour_data)
                
        if tables_data is not None:
            instance.tables.all().delete()
            for table_data in tables_data:
                Table.objects.create(restaurant=instance, **table_data)
                
        return instance