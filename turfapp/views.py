from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from publicapp.models import *
from .forms import *
from userapp.models import Userprofile

# Create your views here.
class Turfownerhomeload(View):
    def get(self, request):
        return render(request, 'turf/turfhome.html')
    
class TurfOwneReg(View):
    def get(self, request):
        form = TurfOwneregForm()  
        return render(request, 'turf/turfownerreg.html', {'form': form})  
    
    def post(self, request):
        form = TurfOwneregForm(request.POST)
        if form.is_valid():
            turf_admin = form.save(commit=False)
            turf_user = Userprofile.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                user_type='TURF'
            )
            turf_user.is_active = False 
            turf_user.save()
            
            turf_admin.loginid = turf_user
            turf_admin.approval_status = False  
            turf_admin.save()
            
            return redirect("userapp:userlogin") 
        else:
            return render(request, 'turf/turfownerreg.html', {'form': form})

class Addturf(View):
    def get(self, request): 
        form = TurfForm()
        return render(request, 'turf/addturf.html', {'form': form})
    
    def post(self, request):
        form = TurfForm(request.POST, request.FILES)
        if form.is_valid():
            turf = form.save(commit=False)
            turf.Ownername = Userprofile.objects.get(id=request.POST.get("userid"))

            turf.save()

            # Get slots from POST data
            slots = request.POST.getlist("slots")
            for slot_time in slots:
                if slot_time.strip():  # Check for non-empty slot
                    Slot.objects.create(
                        turfid=turf,
                        timeslot=slot_time.strip()
                    )

            return HttpResponse('''<script>alert("Turf and slots added successfully.");window.location="/turfapp/view/";</script>''')

        
        return render(request, 'turf/addturf.html', {'form': form})

        
class Viewturf(View):
    def get(self, request):
        try:
            turfs =request.session['user_id']
            requests=Turf.objects.filter(Ownername=turfs)
        except Userprofile.DoesNotExist:
            return HttpResponse("Userprofile not found for the current user.", status=404)
        return render(request, 'turf/viewturf.html', {'turfs': requests})

    
class Deleteturf(View):
    def get(self, request, id):
        try:
            turf = Turf.objects.get(id=id)
            turf.delete() 
            return HttpResponse('''<script>alert("Turf deleted successfully.");window.location="/turfapp/view/";</script>''')
        except Turf.DoesNotExist:
            return render(request, 'turf/viewturf.html', {'error': 'Turf not found'})

       

class Editturf(View):
    def get(self, request, id):
        turf = Turf.objects.get(pk=id)
        form = TurfForm(instance=turf)
        return render(request, 'turf/editturf.html', {'turf': form})
    
    def post(self, request, id):
        turf = Turf.objects.get(pk=id)
        form = TurfForm(request.POST,request.FILES,  instance=turf)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("Turf Edited successfully.");window.location="/turfapp/view/";</script>''')
        return render(request, 'turf/editturf.html', {'turf': form})
    
class Addproduct(View):
    def get(self, request):
        user_id = request.session['user_id']
        user_profile = Userprofile.objects.get(id=user_id)
        turfs = Turf.objects.filter(Ownername=user_profile)  
        return render(request, 'turf/addproduct.html', {'turfs': turfs})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.Ownerid = Userprofile.objects.get(id=request.session['user_id'])
            product.turfid = Turf.objects.get(id=request.POST['turfid'])  
            product.save()
            return HttpResponse('''<script>alert("Product added successfully.");window.location="/turfapp/viewproduct/";</script>''')
        return render(request, 'turf/addproduct.html', {'form': form})
    
class Viewproduct(View):
    def get(self, request):
        try:
            turfs =request.session['user_id']
            requests=Product.objects.filter(Ownerid=turfs)
        except Userprofile.DoesNotExist:
            return HttpResponse("Userprofile not found for the current user.", status=404)
        return render(request, 'turf/viewproduct.html', {'turfs': requests})

class Deleteproduct(View):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
            product.delete() 
            return HttpResponse('''<script>alert("Product Delected successfully.");window.location="/turfapp/viewproduct/";</script>''')
        except Turf.DoesNotExist:
            return render(request, 'turf/viewproduct.html', {'error': 'Turf not found'})
        
class Editproduct(View):
    def get(self, request, id):
        user_id = request.session['user_id']
        user_profile = Userprofile.objects.get(id=user_id)
        turfs = Turf.objects.filter(Ownername=user_profile)  
        product = Product.objects.get(pk=id)
        form = ProductForm(instance=product)
        return render(request, 'turf/editproduct.html', {'product': form, 'turfs': turfs, 'current_turf': product.turfid})

    def post(self, request, id):
        user_id = request.session['user_id']
        user_profile = Userprofile.objects.get(id=user_id)
        turfs = Turf.objects.filter(Ownername=user_profile) 
        product = Product.objects.get(pk=id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.turfid = Turf.objects.get(id=request.POST['turfid'])  
            product.save()
            return HttpResponse('''<script>alert("Product Edited successfully.");window.location="/turfapp/viewproduct/";</script>''')
        return render(request, 'turf/editproduct.html', {'product': form, 'turfs': turfs, 'current_turf': product.turfid})


class updateProfile(View):
    def get(self, request):
        login_id = request.session.get("user_id")
        print(login_id)
        obj = TurfOwner.objects.filter(loginid__id=login_id).first()
        return render(request, 'turf/updateturfprofile.html', {'turf': obj})
    def post(self,request):
        login_id = request.session.get("user_id")
        obj = TurfOwner.objects.filter(loginid__id=login_id).first()
        form = TurfOwneForm(request.POST,request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("successfully updated");window.location="/turfapp/turfhome/"</script>''')
        return HttpResponse('''<script>alert("Failed");window.location="/turfapp/turf_profile/"</script>''')
    
    

class TurfOwnerBookingHistoryView(View):
    def get(self, request):
        owner_id = request.session.get('user_id')  
        owner_turfs = Turf.objects.filter(Ownername_id=owner_id)  
        
        bookings = BookTurf.objects.filter(turf__in=owner_turfs).select_related('user', 'turf', 'slot').order_by('-booking_date')
        
        return render(request, 'turf/viewbooking.html', {'bookings': bookings})
    
class TurfOwnerRentingHistoryView(View):
    def get(self, request):
        owner_id = request.session.get('user_id')  # Get the current logged-in owner's user ID
        owner_turfs = Turf.objects.filter(Ownername_id=owner_id)  # Get the turfs owned by the owner
        
        # Get the rented products for the owner's turfs
        rented_products = RentProduct.objects.filter(turf__in=owner_turfs).select_related('user', 'product', 'turf').order_by('-booking_date')
        
        # Pass rented products to the template for rendering
        return render(request, 'turf/rentinghistory.html', {'rented_products': rented_products})

class ReturnProductView(View):
    def post(self, request, rent_id):
        # Get the rent product by ID
        rent_product = get_object_or_404(RentProduct, id=rent_id)

        # Mark the product as returned
        rent_product.isreturn = True
        rent_product.payment_status = 'COMPLETED'  # Confirm payment status
        rent_product.save()

        # Update the product's available quantity (add one unit back)
        product = rent_product.product
        product.availablequantity = str(int(product.availablequantity) + 1)
        product.save()

        # Redirect back to the renting history page
        return redirect('turfapp:turf_owner_rent_history')