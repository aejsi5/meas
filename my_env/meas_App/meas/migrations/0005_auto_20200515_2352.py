# Generated by Django 3.0.1 on 2020-05-15 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0004_auto_20200515_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Product_number',
            field=models.CharField(max_length=200, verbose_name='Artikelnummer'),
        ),
    ]