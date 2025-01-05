from django.db import models
from userapp.models import Userprofile

# Create your models here.
class TurfOwner(models.Model):
        STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
        loginid = models.OneToOneField(Userprofile, on_delete=models.CASCADE, blank=True, null=True)
        name=models.CharField(max_length=250,null=True,blank=True)
        gender=models.CharField(max_length=250,null=True,blank=True)
        phone=models.CharField(max_length=250,null=True,blank=True)
        email=models.EmailField(null=True,blank=True)
        address=models.CharField(max_length=1000,null=True,blank=True)
        status =models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
        is_active = models.BooleanField(null=False, blank=True, default=True)
        created_at = models.DateTimeField(auto_now=True)
        updated_at= models.DateTimeField(auto_now=True)
        

class Turf(models.Model):
        Ownername = models.ForeignKey(Userprofile, on_delete=models.CASCADE, blank=True, null=True)
        turfname=models.CharField(max_length=250,null=True,blank=True)
        phone=models.CharField(max_length=250,null=True,blank=True)
        image=models.ImageField(upload_to="images/",null=True,blank=True)
        email=models.EmailField(null=True,blank=True)
        address=models.CharField(max_length=1000,null=True,blank=True)
        location=models.CharField(max_length=1000,null=True,blank=True)
        rent=models.FloatField(null=True,blank=True)
        opentime=models.CharField(max_length=1000,null=True,blank=True)
        closingtime=models.CharField(max_length=1000,null=True,blank=True)
        status =models.CharField(max_length=50,default=True)
        is_active = models.BooleanField(null=False, blank=True, default=True)
        created_at = models.DateTimeField(auto_now=True)
        updated_at= models.DateTimeField(auto_now=True)
        

class Slot(models.Model):
        turfid=models.ForeignKey(Turf, on_delete=models.CASCADE, blank=True, null=True)
        timeslot=models.CharField(max_length=1000,null=True,blank=True)
        status =models.CharField(max_length=50,default=False)
        is_active = models.BooleanField(null=False, blank=True, default=True)
        created_at = models.DateTimeField(auto_now=True)
        updated_at= models.DateTimeField(auto_now=True)

class Product(models.Model):
        Ownerid = models.ForeignKey(Userprofile, on_delete=models.CASCADE, blank=True, null=True)
        turfid = models.ForeignKey(Turf, on_delete=models.CASCADE, blank=True, null=True)
        productname=models.CharField(max_length=250,null=True,blank=True)
        category=models.CharField(max_length=250,null=True,blank=True)
        description=models.CharField(max_length=250,null=True,blank=True)
        image=models.ImageField(upload_to="images/",null=True,blank=True)
        price=models.FloatField(null=True,blank=True)
        quantity=models.CharField(max_length=250,null=True,blank=True)
        availablequantity=models.CharField(max_length=250,null=True,blank=True)
        status =models.CharField(max_length=50,default=True)
        is_active = models.BooleanField(null=False, blank=True, default=True)
        created_at = models.DateTimeField(auto_now=True)
        updated_at= models.DateTimeField(auto_now=True)
