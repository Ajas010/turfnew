from django.urls import path

from adminapp.views import *

urlpatterns = [
    path('turf-approvals/', AdminTurfApprovalView.as_view(), name='admin_turf_approval'),
    path('turf/<int:pk>/update-status/', UpdateTurfStatusView.as_view(), name='update_turf_status'),
    path('viewturf/', AdminTurfviewlView.as_view(), name='view_turf_admin'),
    path('viewbookings/', AdminBookingView.as_view(), name='view_bookings_admin'),
    path('viewproducts/', AdminProductView.as_view(), name='view_products_admin'),
    path('viewrentals/', AdminRentProductView.as_view(), name='view_rentals_admin'),

    



]
