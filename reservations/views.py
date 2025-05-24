from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ReservationSerializer
from .repository import ReservationRepository
import logging


logger = logging.getLogger(__name__)



class ReservationCreateView(APIView):
    """
    View to create a new reservation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                reservation = ReservationRepository.create_reservation(serializer.validated_data, request.user)
                if reservation:
                    logger.info(f"Reservation created successfully: {reservation.id}")
                    return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
                return Response({"error": "No available table for the given time."}, status=status.HTTP_400_BAD_REQUEST)
               
            except Exception as e:
                logger.error(f"Error creating reservation: {str(e)}")
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Create your views here.

class ReservationUpdateView(APIView):
    """
    View to update an existing reservation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        serializer = ReservationSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                reservation = ReservationRepository.update_reservation(pk, serializer.validated_data, request.user)
                if reservation:
                    logger.info(f"Reservation updated successfully: {reservation.id}")
                    return Response(ReservationSerializer(reservation).data, status=status.HTTP_200_OK)
                return Response({"error": "Reservation not found or no table available."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Error updating reservation: {str(e)}")
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
class ReservationCancelView(APIView):
    """
    View to cancel an existing reservation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            reservation = ReservationRepository.cancel_reservation(pk, request.user)
            if reservation:
                logger.info(f"Reservation canceled successfully: {reservation.id}")
                return Response({"message": "Reservation canceled successfully."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Reservation not found or already canceled."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error canceling reservation: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)