# Generated by Django 2.2 on 2019-04-05 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venuesapp', '0011_auto_20190405_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoobject',
            name='tech_service_comments',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о сервисе'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='working_hours_winter',
            field=models.TextField(blank=True, null=True, verbose_name='Часы работы зимой'),
        ),
    ]
