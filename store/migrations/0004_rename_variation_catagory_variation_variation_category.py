# Generated by Django 4.0.3 on 2023-05-17 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_variation_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variation',
            old_name='variation_catagory',
            new_name='variation_category',
        ),
    ]
