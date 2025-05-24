from django.urls import path
from .views import ReservationCreateView, ReservationUpdateView, ReservationCancelView


urlpatterns = [
    path('create/', ReservationCreateView.as_view(), name='reservation-create'),
    path('<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation-update'),
    path('<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
]
