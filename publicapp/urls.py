from django.urls import path
from .views import *

urlpatterns = [
    path('register/', PublicregReg.as_view(), name='public-register'),
    path('profile/<int:id>/', UpdateProfileAPIView.as_view(), name='update-profile'),
    path('allturfs/', TurfListView.as_view(), name='turf_list'),
    path('availableslots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('bookturf/', BookTurfView.as_view(), name='book_turf'),
    path('paymenthistory/<int:user_id>/', PaymentHistoryView.as_view(), name='payment-history'),
    path('productlist/<int:turf_id>/', ProductListView.as_view(), name='product-list'),
    path('rentproduct/', RentProductView.as_view(), name='rent-product'),
    path('rentinghistory/<int:user_id>/', RentingHistoryView.as_view(), name='renting_history'),


]
