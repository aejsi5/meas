# Generated by Django 3.0.1 on 2020-06-02 20:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('meas', '0012_auto_20200521_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('Service_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('Service_number', models.CharField(max_length=200, verbose_name='Arbeitspositions-Nummer')),
                ('Service_name', models.CharField(max_length=200, verbose_name='Arbeitspositionsbezeichnung')),
                ('Service_duration', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Zeiteinheiten')),
                ('Service_vf', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Gültig von')),
                ('Service_vu', models.DateTimeField(blank=True, null=True, verbose_name='Gültig bis')),
                ('Service_ia', models.DateTimeField(auto_now=True, verbose_name='Hinzugefügt am')),
                ('Service_deleted', models.BooleanField(default=False, verbose_name='Gelöscht')),
                ('Mandant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meas.Mandant')),
            ],
        ),
    ]
