from django.db import models

from django.conf import settings

from django.utils.timezone import now
from datetime import timedelta
from datetime import datetime 
import json
import math

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
    has_light = models.BooleanField(verbose_name='Наличие освещения', default=False)
    paid = models.CharField(
        verbose_name='Платное посещение', max_length=50, blank=True, null=True)
    is_paid = models.BooleanField(verbose_name='Булевая платность', default=False)
    
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
    last_updated = models.DateTimeField(verbose_name='Дата последнего изменения', default=now)
    has_manual_cahanges = models.BooleanField(verbose_name='Признак наличия ручной правки', default=False)


#    #возвращает рабочие часы в текущий сезон в виде строки Пн: ... 
#    def working_hours(self):
#        pass
    #возвращает текущий сезон
    def get_current_season(self):

        current_date = datetime.strptime("{:%d.%m}".format(datetime.now()), "%d.%m")

        if self.usage_period_winter:
            str_date_interval_winter = self.usage_period_winter
            winter_interval = (self.usage_period_winter).split("-")
            winter_interval_start =  datetime.strptime(winter_interval[0],"%d.%m")
            winter_interval_end = datetime.strptime(winter_interval[0], "%d.%m")
            winter_interval_ny = datetime.strptime("1.1", "%d.%m")
        else:
            return 'summer'

        if self.usage_period_summer:
            str_date_interval_summer = self.usage_period_summer
            summer_interval = (self.usage_period_summer).split("-")
            summer_interval_start = datetime.strptime(summer_interval[0], "%d.%m")
            summer_interval_end = datetime.strptime(summer_interval[1],"%d.%m")
        else:
            return 'winter'
    
        if ((winter_interval_start < current_date <= winter_interval_ny) or (winter_interval_ny <= current_date <= winter_interval_end)):
            return 'winter'
        elif (summer_interval_start <= current_date <= summer_interval_end):
            return 'summer'

    def get_name(self):
        month = now().month
        if ((not self.name_summer) and (not self.name_winter)):
            return self.object_name
        elif (4 <= month < 11) and self.name_summer:
            return self.name_summer
        else:
            return self.name_winter

    
    def get_working_hours(self):
        month = now().month

        if ((not self.working_hours_winter) and (not self.working_hours_summer)):
            return False
        elif (4 <= month < 11) and self.working_hours_summer:
            return get_str_working_hours(self.working_hours_summer)
        else:
            return get_str_working_hours(self.working_hours_winter)



    #возвращате имя в зависимости от текщего сезона
    #нужно предсмотреть вариант выдачи летнего названия в случае, если указан 
    # период с 1.1 по 31.12, как вариант для интервала с 1.4-1.11. Выдавать зимнее название, если летнее пустое и наоборот. 
    def venue_name(self):
        pass

    def get_gistance_to(self,bounds):
        return calc_distanse_betw_points(self.lat, self.lon, bounds)


class Photo(models.Model):

    SEASONS = (
            ('S', 'Лето'),
            ('W', 'Зима'),
        )
    geo_object = models.ForeignKey(
        GeoObject, verbose_name='Объект', on_delete=models.SET_NULL, null=True)
    #event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.SET_NULL, blank=True
    photo = models.ImageField(verbose_name='Фотография', upload_to='photo')
    #author = 
    season = models.CharField(verbose_name='Сезон', max_length=20, choices=SEASONS, default='W')
    is_active = models.BooleanField(
        verbose_name='Признак активности', default=True)
    description = models.TextField(verbose_name='Описание фото', blank=True)
    create_date = models.DateTimeField(verbose_name='Дата загрузки', default=now)
    api_id = models.CharField(verbose_name='Идентификатор в API', max_length=50, blank=True, null=True)
    name = models.CharField(max_length=20,blank=True, null=True)


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


def get_str_working_hours(working_hours):
    result = ''
    working_hours = working_hours.replace("\'", "\"")
    days = json.loads(working_hours)

    for cur_day in days:
  
        result = "{result} {day}: {hours}\n".format(
            result=result, day=cur_day['DayOfWeek'], hours=cur_day['Hours'])

    return result

#получить бдижайшие к центру карты объекты в заданной области 
def get_objects_in_bounds(bounds, **kwargs):
    
    
    center = [(bounds[0][0]+bounds[1][0])/2, (bounds[0][1] + bounds[1][1]) / 2  ]
    venues = GeoObject.objects.filter(is_active=True, lat__range=(bounds[0][0], bounds[1][0]),
                                    lon__range=(bounds[0][1],bounds[1][1] ))
    if kwargs:
        filters = kwargs['filter']
        #print(filters)
        data_filters = {
            'adm_area__in': list(map(lambda x: int(x), filters[0]['adm_area'])),
            'object_type__in': list(map(lambda x: int(x), filters[1]['dataset'])),
        }
        #print(data_filters)
        venues = venues.filter(**data_filters)
        #print(venues.query)
        #print(venues.count())
         #for filter in filters:

    distances = []
    for venue in venues:
        distance = calc_distanse_betw_points(venue.lat, venue.lon, bounds)
        distances.append((venue.pk, distance))
        distances.sort(key=lambda i: i[1])

    return distances[:settings.COUNT_OF_NEAREST_VENUES]

def degrees_to_radians(degrees):
  return degrees * math.pi / 180

#calculate distance between two poinst
def calc_distanse_betw_points(lat1, lon1, bounds):
    
  earth_radius_km = 6371
  center = [(bounds[0][0] + bounds[1][0]) / 2, (bounds[0][1] + bounds[1][1]) / 2]

  d_lat = degrees_to_radians(center[0] - lat1)
  d_lon = degrees_to_radians(center[1] - lon1)

  lat1 = degrees_to_radians(lat1)
  lat2 = degrees_to_radians(center[1])

  a = (math.sin(d_lat/2))**2 + ((math.sin(d_lon/2))**2) * math.cos(lat1) * math.cos(lat2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  return earth_radius_km * c


#для определения ближайших объектов через SQL, не работает в базовом SQLite, не хватает математики.
class Distances(models.Manager):
    def distance(self, bounds):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            select pk, object_name, 
                ( 3959 * acos( cos( radians({center_lat}) ) 
                        * cos( radians( GeoObjects.lat ) ) 
                        * cos( radians( GeoObjects.lon ) - radians({center_lon}) ) 
                        + sin( radians({center_lat}) ) 
                        * sin( radians( GeoObjects.lat ) ) ) ) AS distance 
            from GeoObjects 
            where active = 1 
            and GeoObjects.lat between {bounds_x1} and {bounds_x2} 
            and GeoObjects.lon between {bounds_y1} and {bounds_y2}
            having distance < 10 ORDER BY distance;
        """)
        result_list = []
        for row in cursor.fetchall():
            p = self.model(id=row[0], question=row[1], poll_date=row[2])
            p.num_responses = row[3]
            result_list.append(p)
        return result_list
