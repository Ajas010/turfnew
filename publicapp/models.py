from django.db import models

from turfapp.models import *
from userapp.models import Userprofile

# Create your models here.
class Public(models.Model):
    loginid = models.OneToOneField(Userprofile, on_delete=models.CASCADE, blank=True, null=True)
    name=models.CharField(max_length=250,null=True,blank=True)
    gender=models.CharField(max_length=250,null=True,blank=True)
    phone=models.CharField(max_length=250,null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    address=models.CharField(max_length=1000,null=True,blank=True)
    status =models.CharField(max_length=50,default=True)
    is_active = models.BooleanField(null=False, blank=True, default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at= models.DateTimeField(auto_now=True)

class BookTurf(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE,blank=True, null=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE,blank=True, null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE,blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING',blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    status =models.CharField(max_length=50,default=True)
    is_active = models.BooleanField(null=False, blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

class RentProduct(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE,blank=True, null=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING',blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    isreturn=models.BooleanField(blank=True, null=True,default=False)
    status =models.CharField(max_length=50,default=True)
    is_active = models.BooleanField(null=False, blank=True, default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
