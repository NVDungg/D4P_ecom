from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.ImageField( upload_to='photos/categorys', blank=True)

    class Meta:
        '''Rename model in admin model'''
        verbose_name = 'category'   
        verbose_name_plural = 'categories'

    def get_url(self):
        '''make fucntion reverse to category by slug use url name of store'''
        return reverse('product_category', args=[self.slug])
            #reverse(url_name, args=args, kwargs=kwargs)

    def __str__(self):
        return self.category_name