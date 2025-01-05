from rest_framework import serializers
from .models import *
from userapp.models import *
from turfapp.models import*

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['username', 'password']

class PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Public
        fields = ['name', 'gender', 'phone', 'email', 'address']


class PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Public
        fields = ['name', 'gender', 'phone', 'email', 'address']


class LoginSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, data):
        if 'username' not in data and 'password' not in data:
            raise serializers.ValidationError("No data provided for update.")
        return data
    

class TurfSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        bookings_count = BookTurf.objects.filter(turf=instance, is_active=True).count()
        if bookings_count >= 40:
            rating = 5.0
        elif bookings_count >= 35:
            rating = 4.5
        elif bookings_count >= 30:
            rating = 4.0
        elif bookings_count >= 25:
            rating = 3.5
        elif bookings_count >= 20:
            rating = 3.0
        elif bookings_count >= 15:
            rating = 2.5
        elif bookings_count >= 10:
            rating = 2.0
        elif bookings_count >= 5:
            rating = 1.5
        else:
            rating = 1.0  
        representation['rating'] = rating
        
        return representation

    class Meta:
        model = Turf
        fields = [
            'id', 'turfname', 'phone', 'image', 'email', 
            'address', 'location', 'rent', 'opentime', 
            'closingtime', 'rating'
        ]


class SlotSerializer(serializers.ModelSerializer):
    rent = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['id', 'timeslot', 'status', 'is_active', 'rent']

    def get_rent(self, obj):
        return obj.turfid.rent if obj.turfid else None


class BookTurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTurf
        fields = ['user', 'turf', 'slot', 'booking_date', 'payment_status', 'amount', 'status', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    # To get the full image URL
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Product
        fields = ['id', 'productname', 'category', 'description', 'image', 'price', 'status', 'is_active', 'created_at', 'updated_at','quantity','availablequantity']


class RentProductSerializer(serializers.ModelSerializer):
    productname = serializers.CharField(source='product.productname', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    quantity = serializers.CharField(source='product.quantity', read_only=True)
    availablequantity = serializers.CharField(source='product.availablequantity', read_only=True)

    class Meta:
        model = RentProduct
        fields = [
            'id','productname', 'product_image', 'quantity','availablequantity', 'turf','booking_date','amount','isreturn','status', 'created_at','updated_at',
        ]