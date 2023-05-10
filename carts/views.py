from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView, DeleteView, ListView
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.mixins import Mix
from django.urls import reverse_lazy

from store.models import Product
from .models import Cart, CartItem
# Create your views here.

# No model set
class CartItemView(ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'

    # If you don't set the model. You must implement the get_queryset method to fetch the cart items and return a queryset
    def get_queryset(self):
        try:
            cart = Cart.objects.get(cart_id=_cart_id(self.request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            return cart_items   # This context name ( You can return CartItem.objects.filter(cart=cart, is_active=True) soo u can use any context u naming)
        except ObjectDoesNotExist:
            return CartItem.objects.none()

    def get_context_data(self, **kwargs):
        # Must super get context first. Cause the super here return context cart_item in query set
        context = super().get_context_data(**kwargs)

        # Extend context here
        total = sum([cart_item.product.price * cart_item.quantity for cart_item in self.object_list])
        quantity = sum([cart_item.quantity for cart_item in self.object_list])
        tax = (2 * total)/100
        grand_total = total + tax
        # Will update it below
        context.update({
            'total': total,
            'quantity': quantity,
            'tax':tax,
            'grand_total':grand_total,
        })
        return context
    
# Had model set
'''class ItemCartView(ListView):
model = CartItem
template_name = 'cart/cart.html'

def get_context_data(self, **kwargs):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(self.request))
        cart_items = CartItem.objects.filter(cart=cart, is_active = True)
    except ObjectDoesNotExist:
        pass

    total = sum([cart_item.product.price * cart_item.quantity for cart_item in self.object_list]) 
    quantity = sum([cart_item.quantity for cart_item in self.object_list])
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return context
'''

class CartItemDeleteView(DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart_view')
    template_name = 'cart/cart.html'
    
    def get_object(self, queryset=None):
        product_id = self.kwargs['product_id']
        cart_item_id = self.kwargs['cart_item_id']
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(cart_id=_cart_id(self.request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
        return cart_item
    
    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart_view')

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))  # implement card using cart_id( it session product)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request),
        )
    
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)    #conves product n session product to cart_item in cart
        cart_item.quantity += 1 # increase after click
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('cart_view')

def _cart_id(request):
    cart = request.session.session_key      # get session product 
    if not cart:
        cart = request.session.create()
    return cart