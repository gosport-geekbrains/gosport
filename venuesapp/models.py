from django.db import models

from django.utils.timezone import now
from datetime import timedelta

# Create your models here.


# Create your models here.



class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория объекта', max_length=50, unique=True)
    dataset_id = models.PositiveIntegerField(
        verbose_name='Идентификатор датасета', unique=True)
    marker = models.ImageField(
        verbose_name='Картинка-маркер категории', upload_to='map_markers', default='point_blue')
    description = models.TextField(
        verbose_name='Описание категории объекта', blank=True)
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)
    ya_preset = models.CharField(verbose_name='Yandex settings', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class CategoryClear(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=50)
    description = models.TextField(
        verbose_name='Описание категории', blank=True)
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)

    def __str__(self):
        return self.name


class AdmArea(models.Model):
    name = models.CharField(
        verbose_name='Административный округ', unique=True, max_length=50)
    description = models.CharField(
        verbose_name='Описание округа', blank=True, max_length=50)
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(verbose_name='Район', max_length=50, unique=True)
    #cleared_name = models.CharField(verbose_name='Очищенное название района', blank=True)
    description = models.TextField(verbose_name='Название района', blank=True)
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)

    def __str__(self):
        return self.name


class GeoObject(models.Model):
    global_id = models.PositiveIntegerField(
        verbose_name='Идентификатор объекта')
    object_type = models.ForeignKey(
        Category, verbose_name='Тип объекта', on_delete=models.SET_NULL, null=True)
    category_clear = models.ForeignKey(CategoryClear, verbose_name='Очищенный тип объекта',
                                       on_delete=models.SET_NULL, null=True)
    object_name = models.CharField(
        verbose_name='Название объекта (общее)', max_length=50)
    name_winter = models.CharField(
        verbose_name='Зимнее название', max_length=50, blank=True, null=True)
    name_summer = models.CharField(
        verbose_name='Летнее название', max_length=50, blank=True, null=True)
    adm_area = models.ForeignKey(
        AdmArea, verbose_name='Административный округ', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(
        District, verbose_name='Название района', on_delete=models.SET_NULL, null=True)
    address = models.TextField(
        verbose_name='Адрес объекта', blank=True, null=True)
    email = models.CharField(
        verbose_name='Адрес электронной почты для связи', max_length=50, blank=True, null=True)
    description = models.TextField(
        verbose_name='Описание объекта', blank=True, null=True)
    web_site = models.CharField(
        verbose_name='Адрес сайта', max_length=50, blank=True, null=True)
    help_phone = models.CharField(
        verbose_name='Телефон для связи', max_length=50, blank=True, null=True)
    working_hours_winter = models.TextField(
        verbose_name='Часы работы зимой', blank=True, null=True)
    working_hours_summer = models.TextField(
        verbose_name='Часы работы летом', blank=True, null=True)
    has_equipment_rental = models.BooleanField(
        verbose_name='Наличие проката оборудования', default=False)
    has_tech_service = models.BooleanField(
        verbose_name='Наличие сервиса оборудования', default=False)
    tech_service_comments = models.TextField(
        verbose_name='Информация о сервисе', blank=True, null=True)
    has_dressing = models.BooleanField(
        verbose_name='Наличие раздевалки', default=False)
    has_eatery = models.BooleanField(verbose_name='Наличие еды', default=False)
    has_toilet = models.BooleanField(
        verbose_name='Наличие туалета', default=False)
    has_wifi = models.BooleanField(verbose_name='Наличие WiFi', default=False)
    has_cash_machine = models.BooleanField(
        verbose_name='Наличие банкомата', default=False)
    has_first_aid = models.BooleanField(
        verbose_name='Наличие медицинской помощи', default=False)
    has_music = models.BooleanField(
        verbose_name='Наличие музыки', default=False)
    disability_friendly = models.CharField(
        verbose_name='Приспособлено для инвалидов', max_length=50, blank=True, null=True)
    lighting = models.CharField(
        verbose_name='Освещение', max_length=50, blank=True, null=True)
    paid = models.CharField(
        verbose_name='Платное посещение', max_length=50, blank=True, null=True)
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    geo_data = models.TextField(verbose_name='Гео-JSON')
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)
    usage_period_winter = models.CharField(
        verbose_name='Период использования зимой', max_length=50, blank=True, null=True)
    usage_period_summer = models.CharField(verbose_name='Период использования летом', max_length=50, blank=True, null=True)
    services_winter = models.CharField(
        verbose_name='Зимние возможности', max_length=50, blank=True, null=True)
    services_summer = models.CharField(
        verbose_name='Летние возможности', max_length=50, blank=True, null=True)
    paid_comments = models.TextField(verbose_name='Информация о оплате', blank=True, null=True)
    surface_type_winter = models.CharField(
        verbose_name='Тип зимнего покрытия', max_length=50, blank=True, null=True)
    surface_type_summer = models.CharField(
        verbose_name='Тип летнего покрытия', max_length=50, blank=True, null=True)
    services_winter = models.TextField(
        verbose_name='Зимние сервисы', blank=True, null=True)
    services_summer = models.TextField(
        verbose_name='Летние сервисы', blank=True, null=True)
    equipment_rental_comments = models.TextField(
        verbose_name='Информация о прокате', blank=True, null=True)
    create_date = models.DateTimeField(verbose_name='Дата создания', default=now)
    

    
    #def __str__(self):
    #    return self.name


class Photo(models.Model):
    geo_object = models.ForeignKey(
        GeoObject, verbose_name='Объект', on_delete=models.SET_NULL, null=True)
    #event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.SET_NULL, blank=True
    photo = models.ImageField(verbose_name='Фотография', upload_to='photo')
    #author =
    #upload_date
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)
    description = models.TextField(verbose_name='Описание фото', blank=True)
    create_date = models.DateTimeField(verbose_name='Дата загрузки', default=now)
    #owner

    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(verbose_name='Название датасета', max_length=50)
    dataset_id = models.PositiveIntegerField(
        verbose_name='Идентификатор датасета')
    marker = models.ImageField(verbose_name='Маркер датасета',
                               upload_to='markers', default="markers/point_blue.gif")
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)
    ya_preset = models.CharField(verbose_name='Yandex settings', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
