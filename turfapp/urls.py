from django.urls import path

from turfapp.views import *
app_name = 'turfapp'

urlpatterns = [
    path('turfhome/', Turfownerhomeload.as_view(), name='loadturf'),
    path('register/', TurfOwneReg.as_view(), name='turf_register'),
    path('add/', Addturf.as_view(), name='add_turf'),
    path('view/', Viewturf.as_view(), name='view_turf'),
    path('delete/<int:id>/', Deleteturf.as_view(), name='delete_turf'),
    path('edit/<int:id>/', Editturf.as_view(), name='edit_turf'),
    path('addproduct/', Addproduct.as_view(), name='add_product'),
    path('viewproduct/', Viewproduct.as_view(), name='view_product'),
    path('deleteproduct/<int:id>/', Deleteproduct.as_view(), name='delete_product'),
    path('editproduct/<int:id>/', Editproduct.as_view(), name='edit_product'),
    path('turf_profile/',updateProfile.as_view(),name='turf_profile'),
    path('booking-history/', TurfOwnerBookingHistoryView.as_view(), name='turf_owner_booking_history'),
    path('renting-history/', TurfOwnerRentingHistoryView.as_view(), name='renting_history'),
    path('renting-history/', TurfOwnerRentingHistoryView.as_view(), name='turf_owner_rent_history'),
    path('return-product/<int:rent_id>/', ReturnProductView.as_view(), name='return_product'),  # Add this URL pattern



]
