# Generated by Django 4.2.6 on 2023-11-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villabetel', '0010_account_price_account_waiter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='product',
        ),
        migrations.AddField(
            model_name='account',
            name='products',
            field=models.ManyToManyField(to='villabetel.product'),
        ),
    ]
