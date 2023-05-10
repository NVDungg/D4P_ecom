from typing import Any, Optional
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product
from categorys.models import Category
from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        #retrieves the value of the category_slug parameter from the URL path.
        category_slug = self.kwargs.get('category_slug')
        categories = None
        products = None
        
        if category_slug != None:
            categories = get_object_or_404(Category, slug = category_slug)
            products = Product.objects.filter(category=categories, is_avaiable=True)
        else:
            products = Product.objects.filter(is_avaiable=True)
        context = { 'products': products,
                    'total': Product.objects.count(), }
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        '''
        get_object Return the object the view is displaying
        get the product_slug and category_slug from the URL kwargs and use them
        to retrieve the Product instance using the get_object_or_404 shortcut function.
        We also pass the category__slug argument to filter products by category.
        '''
        #get both slug of category and product to call it in url path
        category_slug = self.kwargs.get('category_slug')
        product_slug = self.kwargs.get('product_slug')

        #Retrieve the product that matches the given category and product slugs.
        product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request), product=self.object).exists()
        context.update({
            'in_cart':in_cart,
        })
        return context
    
    
