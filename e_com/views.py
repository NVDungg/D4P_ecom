from django.views.generic import TemplateView
from django.views.generic import ListView

from store.models import Product, ReviewRating

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_avaiable=True).order_by('created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = ReviewRating.objects.filter(product__in=context['products'], status=True)
        context['reviews'] = reviews
        return context