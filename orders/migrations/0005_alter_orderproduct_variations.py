# Generated by Django 4.1 on 2022-11-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_variationcategory_options_and_more'),
        ('orders', '0004_remove_orderproduct_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
