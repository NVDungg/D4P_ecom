from django.db import models

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

    def __str__(self):
        return self.category_name