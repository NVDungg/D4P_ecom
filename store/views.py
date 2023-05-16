from typing import Any, Optional
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product
from categorys.models import Category
from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        #retrieves the value of the category_slug parameter from the URL path.
        category_slug = self.kwargs.get('category_slug')
        categories = None
        products = None
        
        if category_slug != None:
            categories = get_object_or_404(Category, slug = category_slug)
            products = Product.objects.filter(category=categories, is_avaiable=True).order_by('-created_date')
        else:
            products = Product.objects.filter(is_avaiable=True).order_by('-created_date')
        
        # Paginate the products | paginator is override query to only get enought item = paginate_by
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        paginated_products = paginator.get_page(page)

        context = { 
            'products':paginated_products,  #The products still a query to model but only get item = paginate_by per page
            'total': Product.objects.count(), 
        }
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
        #Check Item in_cart
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request), product=self.object).exists()
        context.update({
            'in_cart':in_cart,
        })
        return context
    
def search(request):
    #products = None
    #product_count = 0
    if 'keyword' in request.GET:    #get name in form by method 
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
    