from django.urls import path
from .views import RegisterView, CustomLoginView, UserDetailView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='user_detail'),
    
    
]