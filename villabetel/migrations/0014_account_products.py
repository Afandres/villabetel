# Generated by Django 4.2.6 on 2023-11-26 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villabetel', '0013_remove_account_products_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='products',
            field=models.ManyToManyField(through='villabetel.ProductQuantity', to='villabetel.product'),
        ),
    ]
