# Generated by Django 4.0.3 on 2023-05-17 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_variation_catagory_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=100),
        ),
    ]
