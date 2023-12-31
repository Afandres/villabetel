# Generated by Django 4.2.6 on 2023-11-30 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('villabetel', '0018_alter_account_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='document_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Documento'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Apellido'),
        ),
    ]
