from rest_framework import serializers
from .models import Restaurant, OpeningHour, Table


class TableSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=False, 
        allow_null=True)

    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'is_outdoor', 'is_available', 'restaurant']
        read_only_fields = ['id'] 

class OpeningHourSerializer(serializers.ModelSerializer):
   
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(),required=False, 
        allow_null=True)

    class Meta:
        model = OpeningHour
        fields = ['id', 'day', 'open_time', 'close_time', 'is_closed', 'restaurant']
        read_only_fields = ['id'] # 'id' is read-only, 'restaurant' is now writable
    
    def validate(self, data):
        if data['open_time'] >= data['close_time']:
            raise serializers.ValidationError("Open time must be before close time.")
        return data



class RestaurantSerializer(serializers.ModelSerializer):
   
    opening_hours = OpeningHourSerializer(many=True, required=False) 
    tables = TableSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone_number', 'owner', 'created_at', 'opening_hours', 'tables']
        read_only_fields = ['id', 'owner', 'created_at']
        
    def create(self, validated_data):
      
        opening_hours_data = validated_data.pop('opening_hours', [])
        tables_data = validated_data.pop('tables', [])
        restaurant = Restaurant.objects.create(**validated_data)
        
        for hour_data in opening_hours_data:
            OpeningHour.objects.create(restaurant=restaurant, **hour_data)
            
        for table_data in tables_data:
            Table.objects.create(restaurant=restaurant, **table_data)
            
        return restaurant 
        
    def update(self, instance, validated_data):
    
        validated_data.pop('opening_hours', None) 
        validated_data.pop('tables', None)
        
        # Update simple fields of the main Restaurant instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
                
        return instance
