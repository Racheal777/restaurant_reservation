from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, OpeningHourViewSet, TableViewSet


router = DefaultRouter()

router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'opening-hours', OpeningHourViewSet, basename='openinghour')
router.register(r'tables', TableViewSet, basename='table')

urlpatterns = [
   
    path('', include(router.urls)),
]
