# Generated by Django 4.0.3 on 2023-06-19 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_productgallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.ImageField(default='photo/productsttl.png', max_length=255, upload_to='photo/products'),
        ),
    ]
