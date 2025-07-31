#!/usr/bin/env python
import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusdish.settings')
django.setup()

from django.contrib.auth.models import User
from vendors.models import Vendor, MenuItem
from accounts.models import Profile

def create_sample_data():
    print("Creating sample data...")
    
    # Create sample vendors
    vendors_data = [
        {
            'name': "Mama Esi's Kitchen",
            'description': "Authentic Ghanaian banku with tilapia and okro stew. Traditional recipes passed down through generations.",
            'rating': Decimal('4.8'),
            'review_count': 120,
            'distance': Decimal('1.8'),
            'delivery_time': "20-30 mins"
        },
        {
            'name': "Kofi's Rice Bowl",
            'description': "Delicious jollof rice and fried rice with chicken, beef, or fish. Fresh ingredients daily.",
            'rating': Decimal('4.5'),
            'review_count': 89,
            'distance': Decimal('2.1'),
            'delivery_time': "25-35 mins"
        },
        {
            'name': "Auntie Akos Soup House",
            'description': "Traditional Ghanaian soups including groundnut soup, palm nut soup, and light soup.",
            'rating': Decimal('4.7'),
            'review_count': 156,
            'distance': Decimal('1.5'),
            'delivery_time': "30-40 mins"
        },
        {
            'name': "Campus Snacks Corner",
            'description': "Quick bites and snacks for busy students. Kelewele, meat pie, and local pastries.",
            'rating': Decimal('4.3'),
            'review_count': 67,
            'distance': Decimal('0.8'),
            'delivery_time': "15-25 mins"
        }
    ]
    
    vendors = []
    for vendor_data in vendors_data:
        vendor, created = Vendor.objects.get_or_create(
            name=vendor_data['name'],
            defaults=vendor_data
        )
        vendors.append(vendor)
        if created:
            print(f"Created vendor: {vendor.name}")
    
    # Create sample menu items
    menu_items_data = [
        # Mama Esi's Kitchen
        {
            'vendor': vendors[0],
            'name': 'Banku with Tilapia',
            'description': 'Traditional banku served with grilled tilapia and spicy okro stew',
            'price': Decimal('25.00'),
            'category': 'other'
        },
        {
            'vendor': vendors[0],
            'name': 'Fufu with Goat Soup',
            'description': 'Fresh fufu with rich goat meat soup and vegetables',
            'price': Decimal('30.00'),
            'category': 'soup'
        },
        
        # Kofi's Rice Bowl
        {
            'vendor': vendors[1],
            'name': 'Jollof Rice with Chicken',
            'description': 'Spicy jollof rice served with grilled chicken and salad',
            'price': Decimal('20.00'),
            'category': 'rice'
        },
        {
            'vendor': vendors[1],
            'name': 'Fried Rice Special',
            'description': 'Fried rice with mixed vegetables, egg, and choice of protein',
            'price': Decimal('22.00'),
            'category': 'rice'
        },
        {
            'vendor': vendors[1],
            'name': 'Plain Rice with Stew',
            'description': 'Steamed rice with tomato stew and fried plantain',
            'price': Decimal('15.00'),
            'category': 'rice'
        },
        
        # Auntie Akos Soup House
        {
            'vendor': vendors[2],
            'name': 'Groundnut Soup',
            'description': 'Rich groundnut soup with chicken and vegetables, served with fufu',
            'price': Decimal('28.00'),
            'category': 'soup'
        },
        {
            'vendor': vendors[2],
            'name': 'Palm Nut Soup',
            'description': 'Traditional palm nut soup with fish and crab, served with banku',
            'price': Decimal('32.00'),
            'category': 'soup'
        },
        {
            'vendor': vendors[2],
            'name': 'Light Soup',
            'description': 'Spicy light soup with goat meat and vegetables',
            'price': Decimal('26.00'),
            'category': 'soup'
        },
        
        # Campus Snacks Corner
        {
            'vendor': vendors[3],
            'name': 'Kelewele',
            'description': 'Spicy fried plantain cubes with ginger and pepper',
            'price': Decimal('8.00'),
            'category': 'snacks'
        },
        {
            'vendor': vendors[3],
            'name': 'Meat Pie',
            'description': 'Flaky pastry filled with seasoned minced meat',
            'price': Decimal('5.00'),
            'category': 'snacks'
        },
        {
            'vendor': vendors[3],
            'name': 'Bofrot',
            'description': 'Sweet Ghanaian donuts, perfect with tea or coffee',
            'price': Decimal('3.00'),
            'category': 'snacks'
        },
        {
            'vendor': vendors[3],
            'name': 'Chin Chin',
            'description': 'Crunchy fried pastry cubes, lightly sweetened',
            'price': Decimal('6.00'),
            'category': 'snacks'
        }
    ]
    
    for item_data in menu_items_data:
        item, created = MenuItem.objects.get_or_create(
            vendor=item_data['vendor'],
            name=item_data['name'],
            defaults=item_data
        )
        if created:
            print(f"Created menu item: {item.name}")
    
    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()