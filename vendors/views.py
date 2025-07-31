from django.shortcuts import render, get_object_or_404
from .models import Vendor, MenuItem

def home(request):
    category = request.GET.get('category', 'all')
    vendors = Vendor.objects.all()
    
    if category != 'all':
        vendors = vendors.filter(menu_items__category=category).distinct()
    
    # Get popular menu items for display
    popular_items = MenuItem.objects.filter(is_available=True)[:12]
    
    context = {
        'vendors': vendors,
        'popular_items': popular_items,
        'current_category': category,
        'categories': ['all', 'rice', 'soup', 'snacks'],
    }
    return render(request, 'vendors/home.html', context)

def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    menu_items = vendor.menu_items.filter(is_available=True)
    
    context = {
        'vendor': vendor,
        'menu_items': menu_items,
    }
    return render(request, 'vendors/vendor_detail.html', context)