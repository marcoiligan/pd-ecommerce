# Generated by Django 4.1 on 2022-11-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amound_paid',
            new_name='amount_paid',
        ),
    ]
