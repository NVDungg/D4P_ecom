from django.views.generic import TemplateView
from django.views.generic import ListView
from store.models import Product

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = { 'products': Product.objects.all().filter(is_avaiable=True), }
        return context