from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView, DeleteView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from store.models import Product, Variation
from .models import Cart, CartItem
# Create your views here.

# No model set
class CartItemView(ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cart_items'

    # If you don't set the model. You must implement the get_queryset method to fetch the cart items and return a queryset
    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=self.request.user, is_active=True).order_by('-id')
            return cart_items
        else:
            '''Check cart exists or not if exists then return list card_item in the cart
            else retun cart item none '''
            try:
                cart = Cart.objects.get(cart_id=_cart_id(self.request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
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
    tax = (2 * total)/100
    grand_total = total + tax
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return context
'''

class CartItemDeleteView(DeleteView):
    model = CartItem
    success_url = reverse_lazy('cart_view')
    
    def get_object(self, queryset=None):
        # Get id of 2
        product_id = self.kwargs.get('product_id')
        cart_item_id = self.kwargs.get('cart_item_id')

        # Get object 
        product = get_object_or_404(Product, id=product_id)

        if self.request.user.is_authenticated:  # Get cart by client session
            cart_item = CartItem.objects.get(product=product, user=self.request.user, id=cart_item_id)
            return cart_item
        else:
            # Get cart by client session
            cart = Cart.objects.get(cart_id=_cart_id(self.request))
            #n conves it to return
            cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
            return cart_item
    
    #We overrides get method to skip comfirm delete( if u don't want use template_comfirm_delete in DeleteView)
    def get(self, request, *args, **kwargs):    
        '''check if cart_item.quantity > 1 before decrementing the quantity and saving the object. 
        If the quantity becomes zero or less, we delete the cart_item directly.'''
        cart_item = self.get_object()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect(self.success_url)
    
class RemoveCartItemView(DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_confirm_delete.html'
    success_url = reverse_lazy('cart_view')

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart_item_id = self.kwargs.get('cart_item_id')

        if self.request.user.is_authenticated:  # Get cart by client session
            cart_item = CartItem.objects.get(product=product, user=self.request.user, id=cart_item_id)
            return cart_item
        else:
            # Get cart by client session
            cart = Cart.objects.get(cart_id=_cart_id(self.request))           
            cart_item = CartItem.objects.get(product=product, cart=cart, id=self.kwargs['cart_item_id'])
            return cart_item

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return redirect(self.success_url)

#same with CartItemView
class CheckoutView(LoginRequiredMixin, ListView):
    template_name = 'store/checkout.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=self.request.user, is_active=True).order_by('-id')
            return cart_items
        else:
            '''Check cart exists or not if exists then return list card_item in the cart
            else retun cart item none '''
            try:
                cart = Cart.objects.get(cart_id=_cart_id(self.request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
                return cart_items   # This context name ( You can return CartItem.objects.filter(cart=cart, is_active=True) soo u can use any context u naming)
            except ObjectDoesNotExist:
                return CartItem.objects.non

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

        for cart_item in context['cart_items']:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

        context.update({
            'total': total,
            'quantity': quantity,
            'tax': tax,
            'grand_total': grand_total,
        })
        return context

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    #if it user authenticated user. Cart it save by user
    if current_user.is_authenticated:
        # below is get product_variation
        product_variation = []
        if request.method == 'POST':
            # get value by name in form
            # instead of get 1 by 1 value color/size = request.POST['color/size'] .We can use for to get every thing form had
            for item in request.POST:
                key = item                  # get the key is name(variation_category) in form (color/size)
                value = request.POST[key]   # store the value of key(variation_value)

                try:
                    #check key n value exact variation category/value, map the name product to variation
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #product_variation it the product had unique variation
                    product_variation.append(variation) #store value in CartItem
                except:
                    pass 

        # below is get cart_item
        # check is_cart_item_exists(had that product in cart)
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists() 
        if is_cart_item_exists:
            #filter cart_item have same product n user in cart
            cart_item = CartItem.objects.filter(product=product, user=current_user)    

            #create variation n id for each product had different variation
            exists_variation = []
            id = []
            for item in cart_item:  
                '''fetch each product in cart_item take the variation had in each product
                store it in exists_variation and store different id of product
                have unique variation in id'''
                existing_variation = item.variations.all()
                exists_variation.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in exists_variation:
                '''if product_variation have item same variation is exists in exists_variation
                go to index of that product and increase  it'''
                index = exists_variation.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1 # increase after click
                item.save()
            else:
                '''create new product had new unique variation. In cart have same user'''
                item = CartItem.objects.create(product=product, quantity = 1 , user=current_user)
                if len(product_variation) > 0:      #check if not empty then add in db
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, user=current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart_view')
    
    #if user not authenticated. Cart it save by session anonymous user(client session)
    else:

        # below is get product_variation
        product_variation = []
        if request.method == 'POST':
            # get value by name in form
            # instead of get 1 by 1 value color/size = request.POST['color/size'] .We can use for to get every thing form had
            for item in request.POST:
                key = item                  # get the key is name(variation_category) in form (color/size)
                value = request.POST[key]   # store the value of key(variation_value)

                try:
                    #check key n value exact variation category/value, map the name product to variation
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #product_variation it the product had unique variation
                    product_variation.append(variation) #store value in CartItem
                except:
                    pass
        
        # below is get cart. 
        """Cause we don't had authenticated user to save cart_item in cart use.
          So we have to take session anonymous user to save cart item in cart"""
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))  # implement card using cart_id( it session user)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request),
            )
        
        cart.save()


        # below is get cart_item
        # check is_cart_item_exists(had that product in cart)
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists() 
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)    #filter cart_item have same product n session user in cart

            #create variation n id for each product had different variation
            exists_variation = []
            id = []
            for item in cart_item:  
                '''fetch each product in cart_item take the variation had in each product
                store it in exists_variation and store different id of product
                have unique variation in id'''
                existing_variation = item.variations.all()
                exists_variation.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in exists_variation:
                '''if product_variation have item same variation is exists in exists_variation
                go to index of that product and increase  it'''
                index = exists_variation.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1 # increase after click
                item.save()
            else:
                '''create new product had new unique variation'''
                item = CartItem.objects.create(product=product, quantity = 1 , cart=cart)
                if len(product_variation) > 0:      #check if not empty then add in db
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart_view')

def _cart_id(request):
    cart = request.session.session_key      #make a cart by get session anonymous user(client session)
    if not cart:
        cart = request.session.create()
    return cart