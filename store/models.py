from django.db import models
from django.urls import reverse
from categorys.models import Category
# Create your models here.
class Product(models.Model):
    product_name = models.CharField( max_length=200 , unique=True)
    slug = models.SlugField( max_length=200, unique=True)
    description = models.TextField( max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField( upload_to='photo/products')
    stock = models.IntegerField()
    is_avaiable = models.BooleanField( default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField( auto_now=False, auto_now_add=False)
    modified_date = models.DateTimeField( auto_now=False, auto_now_add=False)

    def get_url(self):
        #get product_slug through category slug
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name