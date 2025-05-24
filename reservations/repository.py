from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Reservation
from restaurants.models import Table



class ReservationRepository:
    
    @staticmethod
    def is_table_available(restaurant, reservation_time, duration, number_of_guests, exclude_reservation_id=None):
        """
        Check if a table is available for a given time and duration.
        """
        end_time = reservation_time + timedelta(minutes=duration)
        overlapping = Reservation.objects.filter(
            restaurant=restaurant,
            canceled=False,
            reservation_time=end_time,
        ).exclude(id=exclude_reservation_id)
        
        tables = Table.objects.filter(restaurant=restaurant, capacity=number_of_guests).order_by('capacity')
        
        for table in tables:
           has_conflict = overlapping.filter(table=table).exists()
           if not has_conflict:
               return table
           return None
       
       
    @staticmethod
    def create_reservation(data, user):
        with transaction.atomic():
            reservation_time = data.get('reservation_time')
            duration = data.get('duration')
            restaurant = data.get('restaurant')
            number_of_guests = data.get('number_of_guests')
            
            table = ReservationRepository.is_table_available(restaurant, reservation_time, duration, number_of_guests)
            
            if not table:
                return None
            
            reservation = Reservation.objects.create(
                customer=user,
                restaurant=restaurant,
                table=table,
                reservation_time=reservation_time,
                number_of_guests=number_of_guests,
                duration=duration,
                special_requests=data.get('special_requests', '')
            )
            return reservation
        
        
        
    @staticmethod
    def update_reservation(reservation_id, data, user):
        """
        Update an existing reservation.
        """
        reservation = Reservation.objects.filter(id=reservation_id, custome=user, canceled=False).first()
        if not reservation:
            return None
        
        reservation_time = data.get('reservation_time', reservation.reservation_time)
        duration = data.get('duration', reservation.durration)
        number_of_guests = data.get('number_of_guests', reservation.number_of_people)
        
        table = ReservationRepository.is_table_available(reservation.restaurant, reservation_time, duration, number_of_guests, exclude_reservation_id=reservation.id)
        
        if not table:
            return None
        
        reservation.reservation_time = reservation_time
        reservation.durration = duration
        reservation.table = table
        reservation.number_of_people = number_of_guests
        reservation.special_requests = data.get('special_requests', reservation.special_requests)
        
        reservation.save()
        
        return reservation
    
    
    @staticmethod
    def cancel_reservation(reservation_id, user):
        """
        Cancel a reservation.
        """
        reservation = Reservation.objects.filter(id=reservation_id, customer=user, canceled=False).first()
        if not reservation:
            return None
        
        reservation.canceled = True
        reservation.save()
        
        return reservation
        
            

