from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, VendorRegistrationForm, DeliveryPartnerRegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    # Get role from URL parameter
    role = request.GET.get('role', 'customer')
    
    if request.method == 'POST':
        # Choose the appropriate form based on role
        if role == 'vendor':
            form = VendorRegistrationForm(request.POST, request.FILES)
        elif role == 'delivery_partner':
            form = DeliveryPartnerRegistrationForm(request.POST, request.FILES)
        else:
            form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            if role == 'vendor':
                messages.success(request, f'Vendor account created successfully! Please login to continue.')
            elif role == 'delivery_partner':
                messages.success(request, f'Delivery partner account created successfully! Please login to continue.')
            else:
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
            return redirect('accounts:login')
    else:
        # Create the appropriate form based on role
        if role == 'vendor':
            form = VendorRegistrationForm()
        elif role == 'delivery_partner':
            form = DeliveryPartnerRegistrationForm()
        else:
            # Pre-populate the form with the selected role for customer
            initial_data = {'role': role}
            form = CustomUserCreationForm(initial=initial_data)
    
    return render(request, 'accounts/register.html', {'form': form, 'selected_role': role})

def logout_view(request):
    logout(request)
    return redirect('home')