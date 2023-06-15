from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .forms import ReviewForm
from .models import Product, ReviewRating
from categorys.models import Category
from carts.models import CartItem
from orders.models import OrderProduct
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
        
        #check if user have buy this item or not. To that user can write review or not
        try:
            orderproduct = OrderProduct.objects.filter(user=self.request.user, product_id=self.object.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None

        #Get the review
        reviews = ReviewRating.objects.filter(product_id=self.object.id, status=True)

        context.update({
            'in_cart':in_cart,
            'orderproduct':orderproduct,
            'reviews':reviews,
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

def submit_review(request, product_id):
    #get request url
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            '''Check if user have reviewed then change old review with new review'''
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            '''if user don't review make form get value in request.POST save it in db'''
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
    