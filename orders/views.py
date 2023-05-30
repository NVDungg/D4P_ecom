from django.shortcuts import render, redirect

from carts.models import CartItem

# Create your views here.
def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_cout = cart_items.count()
    if cart_cout <= 0:
        return redirect('store')
    
    if request.method == POST:
        form = OrderForm(request.POST)