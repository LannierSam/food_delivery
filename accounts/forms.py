from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, initial='customer')
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "phone")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data["role"],
                phone=self.cleaned_data["phone"]
            )
        return user

class VendorRegistrationForm(UserCreationForm):
    # Basic fields
    email = forms.EmailField(required=True)
    
    # Vendor specific fields
    business_name = forms.CharField(max_length=200, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    business_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    business_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)
    business_license = forms.FileField(required=True, help_text="Upload your business license document")
    profile_picture = forms.ImageField(required=False, help_text="Upload your profile picture")
    
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and attributes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.widget.attrs.update({'required': 'required'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # Use email as username
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                role='vendor',
                phone=self.cleaned_data["phone_number"],
                business_name=self.cleaned_data["business_name"],
                business_address=self.cleaned_data["business_address"],
                business_description=self.cleaned_data["business_description"],
                business_license=self.cleaned_data["business_license"],
                profile_picture=self.cleaned_data.get("profile_picture")
            )
        return user

class DeliveryPartnerRegistrationForm(UserCreationForm):
    # Basic fields
    email = forms.EmailField(required=True)
    
    # Delivery partner specific fields
    full_name = forms.CharField(max_length=200, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    vehicle_type_number = forms.CharField(max_length=100, required=True, help_text="e.g., Motorcycle - ABC123")
    drivers_license = forms.FileField(required=True, help_text="Upload your driver's license")
    emergency_contact_name = forms.CharField(max_length=200, required=True)
    emergency_contact_phone = forms.CharField(max_length=15, required=True)
    vehicle_photo = forms.ImageField(required=True, help_text="Upload a photo of your vehicle")
    profile_picture = forms.ImageField(required=False, help_text="Upload your profile picture")
    
    class Meta:
        model = User
        fields = ("email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and attributes
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field.required:
                field.widget.attrs.update({'required': 'required'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]  # Use email as username
        if commit:
            user.save()
            profile = Profile.objects.create(
                user=user,
                role='delivery_partner',
                phone=self.cleaned_data["phone_number"],
                full_name=self.cleaned_data["full_name"],
                vehicle_type_number=self.cleaned_data["vehicle_type_number"],
                drivers_license=self.cleaned_data["drivers_license"],
                emergency_contact_name=self.cleaned_data["emergency_contact_name"],
                emergency_contact_phone=self.cleaned_data["emergency_contact_phone"],
                vehicle_photo=self.cleaned_data["vehicle_photo"],
                profile_picture=self.cleaned_data.get("profile_picture")
            )
        return user