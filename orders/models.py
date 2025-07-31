from django.db import models
from django.contrib.auth.models import User
from vendors.models import MenuItem

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.TextField()
    phone = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)
    service_fee = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.customer:
            return f"Order #{self.id} - {self.customer.username}"
        else:
            return f"Order #{self.id} - {self.customer_name}"
    
    @property
    def subtotal(self):
        return self.total - self.delivery_fee - self.service_fee

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.price

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        elif self.session_key:
            return f"Cart - Anonymous ({self.session_key[:8]})"
        return "Cart - Unknown"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'menu_item')
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.menu_item.price

class OrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for Order #{self.order.id} - {self.vendor.name}"