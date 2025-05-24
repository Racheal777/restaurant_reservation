from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserRepository:
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        """
        try:
            return UserModel.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def create_user(**kwargs):
        """
        Create a new user with the provided keyword arguments.
        """
        user = UserModel.objects.create_user(**kwargs)
        user.save()
        return user
    
    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email address.
        """
        return UserModel.objects.filter(email=email).first()

       
    
    