from .models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_count': cart.total_items}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
    else:
        # Handle anonymous users with session-based carts
        session_key = request.session.session_key
        if session_key:
            try:
                cart = Cart.objects.get(session_key=session_key)
                return {'cart_count': cart.total_items}
            except Cart.DoesNotExist:
                return {'cart_count': 0}
    return {'cart_count': 0}