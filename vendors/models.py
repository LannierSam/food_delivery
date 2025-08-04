from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='vendors/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.IntegerField(default=0)
    distance = models.DecimalField(max_digits=5, decimal_places=1, help_text="Distance in km")
    delivery_time = models.CharField(max_length=20, help_text="e.g., 20-30 mins")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('rice', 'Rice'),
        ('soup', 'Soup'),
        ('snacks', 'Snacks'),
        ('other', 'Other'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.vendor.name}"
    
    def get_default_image(self):
        """Return a default static image path based on the menu item name"""
        name_lower = self.name.lower()
        
        # Map food names to static images
        image_mapping = {
            'banku': 'img/Banku.jpeg.jpg',
            'jollof': 'img/Jollof.jpg',
            'fried rice': 'img/Fried rice.jpg',
            'rice': 'img/Rice with stew.jpg',
            'fufu': 'img/Fufu.jpg',
            'waakye': 'img/waakye.jpg',
            'kenkey': 'img/Kenkey.jpg',
            'beans': 'img/Beans.jpg',
            'spaghetti': 'img/spag.jpg',
            'spag': 'img/spag.jpg',
            'gob3': 'img/G)b3.jpg',
            'gobe': 'img/G)b3.jpg',
            'apesie': 'img/Apesie.jpg',
            'groundnut soup': 'img/peanut_soup.webp',
            'palm nut soup': 'img/palmnut soup.jpg',
            'light soup': 'img/lightsoup.jpg',
            'kelewele': 'img/Kelewele.jpg',
            'meat pie': 'img/meat pie.jpg',
            'chin chin': 'img/chin chin.jpg',
            'bofrot': 'img/bofrot.jpg',
        }
        
        # Check for exact matches first
        for key, image_path in image_mapping.items():
            if key in name_lower:
                return image_path
        
        # Return None if no match found (will show placeholder)
        return None