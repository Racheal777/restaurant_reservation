from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from restaurants.models import OpeningHour, Table
from .repository import RestaurantRepository
from .serializers import RestaurantSerializer, OpeningHourSerializer, TableSerializer
import logging

logger = logging.getLogger(__name__)

class IsOwnerUser(permissions.BasePermission):
    """
    Custom permission to only allow users with 'OWNER' role to access certain views.
    Assumes request.user has a 'role' attribute.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role == 'OWNER'

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating and deleting restaurants.
    """
    queryset = RestaurantRepository.get_all_restaurants()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerUser]

    def get_queryset(self):
        """
        Ensures users only see restaurants they own.
        """
        return self.queryset.filter(owner=self.request.user)


    def perform_create(self, serializer):
        """
        Handles the creation of a Restaurant, passing the owner to the repository.
        The serializer's create method will handle nested opening_hours and tables.
        """
        try:
           
            RestaurantRepository.create_restaurant(serializer, self.request.user)
            logger.info(f"Restaurant created successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error creating restaurant by user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not create restaurant.'}) # Re-raise as serializer error



    def perform_update(self, serializer):
        """
        Handles the update of a Restaurant, calling the repository method.
        """
        try:
        
            updated_restaurant = RestaurantRepository.update_restaurant(
                serializer.instance.id,
                self.request.user,
                serializer.validated_data
            )
            logger.info(f"Restaurant with ID {updated_restaurant.id} updated successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error updating restaurant with ID {serializer.instance.id} by user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not update restaurant.'})



    def perform_destroy(self, instance):
        """
        Handles the deletion of a Restaurant, calling the repository method.
        """
        try:
            RestaurantRepository.delete_restaurant(instance)
            logger.info(f"Restaurant with ID {instance.id} deleted successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error deleting restaurant with ID {instance.id} by user {self.request.user.username}.")
            raise Response({'detail': 'Could not delete restaurant.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OpeningHourViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating and deleting opening hours.
    """
    queryset = OpeningHour.objects.all() # Initial queryset
    serializer_class = OpeningHourSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerUser]
    
    

    def get_queryset(self):
        """
        Ensures users only see opening hours for restaurants they own.
        """
        return self.queryset.filter(owner=self.request.user)
    
    

    def perform_create(self, serializer):
        """
        Handles the creation of an OpeningHour, calling the repository method.
        The client must provide 'restaurant' ID in the request body.
        """
        try:
            restaurant_id = serializer.validated_data.get('restaurant').id # Get the Restaurant object's ID
            RestaurantRepository.create_opening_hour(
                restaurant=restaurant_id,
                owner=self.request.user,
                data=serializer.validated_data
            )
            logger.info(f"Opening hour created for restaurant {restaurant_id} by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error creating opening hour for user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not create opening hour. Check restaurant ID and ownership.'})

    def perform_update(self, serializer):
        """
        Handles the update of an OpeningHour, calling the repository method.
        """
        try:
            updated_opening_hour = RestaurantRepository.update_opening_hour(
                id=serializer.instance.id,
                owner=self.request.user,
                data=serializer.validated_data
            )
            logger.info(f"Opening hour with ID {updated_opening_hour.id} updated successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error updating opening hour with ID {serializer.instance.id} by user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not update opening hour.'})



    def perform_destroy(self, instance):
        """
        Handles the deletion of an OpeningHour, calling the repository method.
        """
        try:
            RestaurantRepository.delete_opening_hour(instance)
            logger.info(f"Opening hour with ID {instance.id} deleted successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error deleting opening hour with ID {instance.id} by user {self.request.user.username}.")
            raise Response({'detail': 'Could not delete opening hour.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TableViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing, creating, retrieving, updating and deleting tables.
    """
    queryset = Table.objects.all() # Initial queryset
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerUser]



    def get_queryset(self):
        """
        Ensures users only see tables for restaurants they own.
        """
        return self.queryset.filter(owner=self.request.user)




    def perform_create(self, serializer):
        """
        Handles the creation of a Table, calling the repository method.
        The client must provide 'restaurant' ID in the request body.
        """
        try:
            restaurant_id = serializer.validated_data.get('restaurant').id # Get the Restaurant object's ID
            RestaurantRepository.create_table(
                restaurant=restaurant_id,
                owner=self.request.user,
                data=serializer.validated_data
            )
            logger.info(f"Table created for restaurant {restaurant_id} by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error creating table for user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not create table. Check restaurant ID and ownership.'})



    def perform_update(self, serializer):
        """
        Handles the update of a Table, calling the repository method.
        """
        try:
            updated_table = RestaurantRepository.update_table(
                id=serializer.instance.id,
                owner=self.request.user,
                data=serializer.validated_data
            )
            logger.info(f"Table with ID {updated_table.id} updated successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error updating table with ID {serializer.instance.id} by user {self.request.user.username}.")
            raise serializers.ValidationError({'detail': 'Could not update table.'})




    def perform_destroy(self, instance):
        """
        Handles the deletion of a Table, calling the repository method.
        """
        try:
            RestaurantRepository.delete_table(instance)
            logger.info(f"Table with ID {instance.id} deleted successfully by user {self.request.user.username}.")
        except Exception as e:
            logger.exception(f"Error deleting table with ID {instance.id} by user {self.request.user.username}.")
            raise Response({'detail': 'Could not delete table.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

