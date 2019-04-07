# Generated by Django 2.2 on 2019-04-05 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venuesapp', '0013_auto_20190405_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoobject',
            name='surface_type_summer',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Тип летнего покрытия'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='surface_type_winter',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Тип зимнего покрытия'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='usage_period_summer',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Период использования летом'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='usage_period_winter',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Период использования зимой'),
        ),
    ]
