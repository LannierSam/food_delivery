from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Food Vendor'),
        ('delivery_partner', 'Delivery Partner'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Vendor specific fields
    business_name = models.CharField(max_length=200, blank=True)
    business_address = models.TextField(blank=True)
    business_description = models.TextField(blank=True)
    business_license = models.FileField(upload_to='business_licenses/', blank=True, null=True)
    
    # Delivery partner specific fields
    full_name = models.CharField(max_length=200, blank=True)
    vehicle_type_number = models.CharField(max_length=100, blank=True)
    drivers_license = models.FileField(upload_to='drivers_licenses/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    vehicle_photo = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    
    # Profile picture for all users
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"