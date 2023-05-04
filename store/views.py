from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Product
from categorys.models import Category

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
    
