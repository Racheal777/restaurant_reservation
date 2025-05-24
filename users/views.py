from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserSerializer, UserRegisterSerializer, CustomTokenObtainPairSerializer
import logging
from .repository import UserRepository
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        logger.info(f"Registering user with data: {request.data}")
        if serializer.is_valid():
            
            try:
                user = UserRepository.create_user(**serializer.validated_data)
                logger.info(f"User created successfully: {user.username}")
                return Response({"message":"User created"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.exception(f"Error creating user: {e}")
            return Response({"error":"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logger.warning(f"Invalid data provided for user registration: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
  
        
    
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
   
    
    
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
    
    