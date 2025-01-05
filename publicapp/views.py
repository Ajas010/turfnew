from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from userapp.models import *
from rest_framework.permissions import IsAuthenticated

class PublicregReg(APIView):
    def get(self, request):
        public_users = Public.objects.filter(is_active=True)
        serializer = PublicSerializer(public_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = PublicSerializer(data=request.data)
        if serializer.is_valid():
            try:
                username = request.data.get('username')
                password = request.data.get('password')
                public_user = Userprofile.objects.create_user(
                    username=username,
                    password=password,
                    user_type='PUBLIC'
                )
                public_instance = serializer.save()
                public_instance.loginid = public_user
                public_instance.save()
                response_data = serializer.data
                response_data['username'] = username
                response_data['password'] = password
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileAPIView(APIView):
    permission_classes=[AllowAny]
    def get_object(self, id):
        try:
            return Public.objects.get(loginid__id=id)
        except Public.DoesNotExist:
            return None

    def get(self, request, id):
        public_user = self.get_object(id)
        if not public_user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PublicSerializer(public_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        permission_classes = [IsAuthenticated]

        public_user = self.get_object(id)
        if not public_user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PublicSerializer(public_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TurfListView(APIView):
    def get(self, request):
        turfs = Turf.objects.all()
        serializer = TurfSerializer(turfs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AvailableSlotsView(APIView):
    def get(self, request):
        turf_id = request.GET.get('turf_id')
        booking_date = request.GET.get('booking_date')

        if not turf_id or not booking_date:
            return Response({"error": "turf_id and booking_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from datetime import datetime
            booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        slots = Slot.objects.filter(turfid=turf_id, is_active=True)

        booked_slots = BookTurf.objects.filter(
            turf_id=turf_id,
            booking_date=booking_date
        ).values_list('slot_id', flat=True)

        turf = Turf.objects.filter(id=turf_id, is_active=True).first()
        if not turf:
            return Response({"error": "Turf not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        slot_data = []
        for slot in slots:
            slot_data.append({
                'id': slot.id,
                'timeslot': slot.timeslot,
                'status': 'True' if slot.id in booked_slots else 'False',
                'is_active': slot.is_active,
                'turf_rent': turf.rent  
            })

        return Response(slot_data, status=status.HTTP_200_OK)


class BookTurfView(APIView):
    def post(self, request):
        turf_id = request.data.get('turf_id')
        slot_id = request.data.get('slot_id')
        booking_date = request.data.get('booking_date')
        user_id = request.data.get('user_id')

        if not all([turf_id, slot_id, booking_date, user_id]):
            return Response(
                {"error": "turf_id, slot_id, booking_date, and user_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from datetime import datetime
            booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        turf = Turf.objects.filter(id=turf_id, is_active=True).first()
        if not turf:
            return Response({"error": "Turf not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        slot = Slot.objects.filter(id=slot_id, turfid=turf, is_active=True).first()
        if not slot:
            return Response({"error": "Slot not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        if BookTurf.objects.filter(turf_id=turf_id, slot_id=slot_id, booking_date=booking_date, is_active=True).exists():
            return Response({"error": "This slot is already booked for the selected date."}, status=status.HTTP_400_BAD_REQUEST)

        user = Userprofile.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            booking = BookTurf.objects.create(
                user=user,
                turf=turf,
                slot=slot,
                booking_date=booking_date,
                payment_status='COMPLETED',
                amount=turf.rent,  
                status="CONFIRMED",
                is_active=True
            )
            return Response({"message": "Booking successful!", "booking_id": booking.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Booking failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
 
class PaymentHistoryView(APIView):
    def get(self, request, user_id):
        user = Userprofile.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        bookings = BookTurf.objects.filter(user=user, is_active=True).order_by('-created_at')

        payment_history = []
        for booking in bookings:
            turf_image_url = booking.turf.image.url if booking.turf.image else None

            payment_history.append({
                'booking_id': booking.id,
                'turf_name': booking.turf.turfname, 
                'slot_time': booking.slot.timeslot, 
                'booking_date': booking.booking_date,
                'payment_status': booking.payment_status,
                'amount': booking.amount,
                'status': booking.status,
                'turf_image': turf_image_url,  
            })

        return Response(payment_history, status=status.HTTP_200_OK)
    

class ProductListView(APIView):
    def get(self, request, turf_id):
        products = Product.objects.filter(turfid=turf_id, is_active=True)
        
        if not products:
            return Response({"error": "No products found for this turf."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RentProductView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        turf_id = request.data.get('turf')
        booking_date = request.data.get('booking_date')
        amount = request.data.get('amount')

        if not user_id or not product_id or not turf_id or not booking_date or not amount:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if int(product.availablequantity) <= 0:
                return Response({"error": "Product is not available."}, status=status.HTTP_400_BAD_REQUEST)
            
            product.availablequantity = str(int(product.availablequantity) - 1)
            product.save()

            rent_product = RentProduct.objects.create(
                user_id=user_id,
                turf_id=turf_id,
                product=product,
                booking_date=booking_date,
                amount=amount,
                payment_status='COMPLETED',  
                isreturn=False,
                status='ACTIVE'
            )

            serializer = RentProductSerializer(rent_product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)



class RentingHistoryView(APIView):
    def get(self, request, user_id):
        try:
            rent_history = RentProduct.objects.filter(user_id=user_id, is_active=True).order_by('-created_at')

            if not rent_history.exists():
                return Response({"message": "No renting history found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = RentProductSerializer(rent_history, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Something went wrong.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)