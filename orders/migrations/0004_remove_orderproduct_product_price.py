# Generated by Django 4.1 on 2022-11-07 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='product_price',
        ),
    ]
