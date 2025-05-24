from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .repository import RestaurantRepository
from .serializers import RestaurantSerializer, OpeningHourSerializer, TableSerializer

# Create your views here.

logger = logging.getLogger(__name__)

class IsOwnerUser(permissions.BasePermission):
    """
    Custom permission to only allow owners to access certain views.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'owner'

class RestaurantListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerUser]

    def get(self, request):
        """
        Retrieve all restaurants.
        """
        restaurants = RestaurantRepository.get_all_restaurants()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new restaurant.
        """
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            restaurant = RestaurantRepository.create_restaurant(serializer, request.user)
            return Response(RestaurantSerializer(restaurant).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RestaurantDetailView(APIView):
  
  
    permission_classes = [permissions.IsAuthenticated, IsOwnerUser]
    
    
    
    def get_object(self, pk, user):
        """
        Helper method to get a restaurant object by ID.
        """
        try:
           
            restaurant = RestaurantRepository.get_restaurant_by_id(pk)
            if restaurant.owner != user:
                raise PermissionError("You do not have permission to access this restaurant.")
            return restaurant
        except Exception as e:
            logger.error(f"Error retrieving restaurant with ID {pk}: {str(e)}")
            return None


    def get(self, request, pk):
        """
        Retrieve a specific restaurant by ID.
        """
        restaurant = self.get_object(pk, request.user)
        if not restaurant:
            return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
       


    def put(self, request, pk):
        """
        Update a specific restaurant by ID.
        """
        restaurant = self.get_object(pk, request.user)
        if not restaurant:
            return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        # Validate and update the restaurant data
        serializer = RestaurantSerializer(restaurant, data=request.data)
        if serializer.is_valid():
            restaurant = RestaurantRepository.update_restaurant(pk, serializer.validated_data)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, restaurant_id):
        """
        Delete a specific restaurant by ID.
        """
      
        restaurant = self.get_object(restaurant_id, request.user)
        if not restaurant:
            return Response({"detail": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        RestaurantRepository.delete(restaurant)
        return Response({"detail": "Deleted successfully."},status=status.HTTP_204_NO_CONTENT)
       