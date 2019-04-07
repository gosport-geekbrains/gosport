# Generated by Django 2.2 on 2019-04-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venuesapp', '0010_auto_20190405_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoobject',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес объекта'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание объекта'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='equipment_rental_comments',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о прокате'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='services_summer',
            field=models.TextField(blank=True, null=True, verbose_name='Летние сервисы'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='services_winter',
            field=models.TextField(blank=True, null=True, verbose_name='Зимние сервисы'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='working_hours_summer',
            field=models.TextField(blank=True, null=True, verbose_name='Часы работы летом'),
        ),
    ]
