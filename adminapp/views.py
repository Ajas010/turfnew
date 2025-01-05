from django.shortcuts import redirect, render
from django.views import View

from publicapp.models import *
from turfapp.models import *

# Create your views here.

class AdminTurfApprovalView(View):
    def get(self, request):
        turf_registrations = TurfOwner.objects.all()
        return render(request, 'admin/tirfownerapprovallist.html', {'users': turf_registrations})
    
class UpdateTurfStatusView(View):
    def post(self, request, pk):
        turf = TurfOwner.objects.get(id=pk)
        action = request.POST.get('action')

        if action == 'approve':
            turf.status = 'approved'
            turf.loginid.is_active = True 
            turf.loginid.save()
        elif action == 'reject':
            turf.status = 'rejected'
            turf.loginid.is_active = False 
            turf.loginid.save()

        turf.save()
        return redirect('admin_turf_approval')
    
class AdminTurfviewlView(View):
    def get(self, request):
        turf_list = Turf.objects.all()  # Fetch all turf objects
        return render(request, 'admin/viewturf.html', {'turf_list': turf_list})
    
class AdminBookingView(View):
    def get(self, request):
        # Fetch all booking records
        bookings = BookTurf.objects.all()
        return render(request, 'admin/view_bookings.html', {'bookings': bookings})
    
class AdminProductView(View):
    def get(self, request):
        # Fetch all products
        products = Product.objects.all()
        return render(request, 'admin/view_products.html', {'products': products})

class AdminRentProductView(View):
    def get(self, request):
        # Fetch all rental records
        rentals = RentProduct.objects.all()
        return render(request, 'admin/view_rentals.html', {'rentals': rentals})