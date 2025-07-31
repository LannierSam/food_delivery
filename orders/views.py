from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from .models import Cart, CartItem, Order, OrderItem
from vendors.models import MenuItem
from .forms import CheckoutForm

def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    # Handle anonymous users with session-based carts
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{menu_item.name} added to cart!')
    return redirect('vendors:vendor_detail', vendor_id=menu_item.vendor.id)

def cart_view(request):
    # Handle anonymous users with session-based carts
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []
            cart = None
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_items = cart.items.all()
            except Cart.DoesNotExist:
                cart_items = []
                cart = None
        else:
            cart_items = []
            cart = None
    
    delivery_fee = Decimal('5.00')
    service_fee = Decimal('2.00')
    subtotal = cart.subtotal if cart else Decimal('0.00')
    total = subtotal + delivery_fee + service_fee
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'service_fee': service_fee,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)

def update_cart_item(request, cart_item_id):
    # Handle anonymous users with session-based carts
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__session_key=session_key)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()
    
    return redirect('orders:cart')

def remove_from_cart(request, cart_item_id):
    # Handle anonymous users with session-based carts
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__session_key=session_key)
    
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('orders:cart')

def checkout(request):
    # Handle anonymous users with session-based carts
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []
            cart = None
    else:
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                cart_items = cart.items.all()
            except Cart.DoesNotExist:
                cart_items = []
                cart = None
        else:
            cart_items = []
            cart = None
    
    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('orders:cart')
    
    delivery_fee = Decimal('5.00')
    service_fee = Decimal('2.00')
    subtotal = cart.subtotal if cart else Decimal('0.00')
    total = subtotal + delivery_fee + service_fee
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order without requiring user login
            order = Order.objects.create(
                total=total,
                delivery_address=form.cleaned_data['delivery_address'],
                phone=form.cleaned_data['phone'],
                customer_name=form.cleaned_data['full_name'],
                delivery_fee=delivery_fee,
                service_fee=service_fee,
            )
            
            # Create order items and notifications for vendors
            vendors_notified = set()
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item.menu_item,
                    quantity=cart_item.quantity,
                    price=cart_item.menu_item.price,
                )
                
                # Create notification for vendor
                vendor = cart_item.menu_item.vendor
                if vendor not in vendors_notified:
                    OrderNotification.objects.create(
                        order=order,
                        vendor=vendor,
                        message=f"New order #{order.id} from {order.customer_name} for {cart_item.menu_item.name}"
                    )
                    vendors_notified.add(vendor)
            
            # Clear cart
            if cart:
                cart.delete()
            
            # Redirect to order confirmation page with order ID
            return redirect('orders:order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'service_fee': service_fee,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'orders/order_confirmation.html', context)