# Generated by Django 3.0.1 on 2020-04-04 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meas_user',
            name='Mandant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='meas.Mandant'),
        ),
    ]
