from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
import requests
import json
import sys

#from venuesapp.models import CategoryClear
from venuesapp.models import Category, GeoObject, District, AdmArea, Photo, Dataset

from venuesapp.views import load_from_json, get_json_from_api, str_to_boolean, get_photo_from_api, lighting_translate

JSON_PATH = 'venuesapp/json'

STR_FEATURES = '[]'

#MAP_JS_PATH = '\static\json'




class Command(BaseCommand):
    help = 'Fill DB new data'

    def add_arguments(self, parser):
        parser.add_argument('--clear',
                            action='store_true',
                            help='clear DB before filling')
    def handle(self, *args, **options):

        datasets = load_from_json('datasets')


        if options['clear']:
            GeoObject.objects.all().delete()
            Dataset.objects.all().delete()
            AdmArea.objects.all().delete()
            District.objects.all().delete()
            Category.objects.all().delete()
            Photo.objects.all().delete()

        for dataset in datasets:

            new_dataset = Dataset(**dataset)
            
            if Dataset.objects.filter(name=dataset['name']).exists():
      
                new_dataset = Dataset.objects.get(name=dataset['name'])
            new_dataset.save()
            
            new_category = Category(**dataset)
            if Category.objects.filter(name=dataset['name']).exists():

                new_category = Category.objects.get(name=dataset['name'])
            new_category.save()

            geo_objects = get_json_from_api(dataset['dataset_id'], STR_FEATURES)
            
            #на случай сохранения данных датасета в json
            #with open(dataset['dataset_id']+'.json', 'w', encoding='utf-8') as f:
            #    json.dump(geo_objects, f, ensure_ascii=False)
           

            for geo_object in geo_objects['features']:
                venue = {}

                venue['global_id'] = geo_object['properties']['Attributes']['global_id']

                if GeoObject.objects.filter(global_id=venue['global_id']).exists():
                    venue['pk'] = GeoObject.objects.get(global_id=venue['global_id']).pk


                adm_area = geo_object['properties']['Attributes']['AdmArea'].replace('административный округ', '').strip()
                if AdmArea.objects.filter(name=adm_area).exists() == False:
                  
                    new_adm_area = AdmArea(name=adm_area)
                    new_adm_area.save()
                venue['adm_area'] = AdmArea.objects.get(name=adm_area)
                
                district = geo_object['properties']['Attributes']['District'].replace('район', '')
                district = district.strip()
                if District.objects.filter(name=district).exists() == False:
                    new_district = District(name=district)
                    new_district.save()
                
                venue['district'] = District.objects.get(name=district)
                
                _category_type = Category.objects.get(name=dataset['name'])
                venue['object_type'] = _category_type
                venue['object_name'] = geo_object['properties']['Attributes']['ObjectName']
                #если заданы зимние параметры - обновляем/заполняем их, не трогая летние
                if 'NameWinter' in geo_object['properties']['Attributes']:
                    venue['name_winter'] = geo_object['properties']['Attributes']['NameWinter']
                    venue['working_hours_winter'] = geo_object['properties']['Attributes']['WorkingHoursWinter']
                    venue['services_winter'] = geo_object['properties']['Attributes']['ServicesWinter']
                    venue['surface_type_winter'] = geo_object['properties']['Attributes']['SurfaceTypeWinter']
                    venue['usage_period_winter'] = geo_object['properties']['Attributes']['UsagePeriodWinter']

                #Если заданы летние параметры обновляем/заполняем их, не трогая зиние
                if 'NameSummer' in geo_object['properties']['Attributes']:
                    venue['name_summer'] = geo_object['properties']['Attributes']['NameSummer']
                    venue['working_hours_summer'] = geo_object['properties']['Attributes']['WorkingHoursSummer']
                    venue['services_summer'] = geo_object['properties']['Attributes']['ServicesWinter']
                    venue['surface_type_summer'] = geo_object['properties']['Attributes']['SurfaceTypeSummer']
                    venue['surface_type_Summer'] = geo_object['properties']['Attributes']['SurfaceTypeSummer']
                    venue['usage_period_summer'] = geo_object['properties']['Attributes']['UsagePeriodSummer']

                venue['address'] = geo_object['properties']['Attributes']['Address']
                venue['email'] = geo_object['properties']['Attributes']['Email']
                venue['web_site'] = geo_object['properties']['Attributes']['WebSite']
                venue['help_phone'] = geo_object['properties']['Attributes']['HelpPhone'] 
                #\+ " " +\str(geo_object['properties']['Attributes']['HelpPhoneExtension'])
 
                venue['has_equipment_rental'] = str_to_boolean(geo_object['properties']['Attributes']['HasEquipmentRental'])
                venue['has_tech_service'] = str_to_boolean(geo_object['properties']['Attributes']['HasTechService'])
                venue['tech_service_comments'] = geo_object['properties']['Attributes']['TechServiceComments']
                venue['has_dressing'] = str_to_boolean(geo_object['properties']['Attributes']['HasDressingRoom'])
                venue['has_eatery'] = str_to_boolean(geo_object['properties']['Attributes']['HasEatery'])
                venue['has_toilet'] = str_to_boolean(geo_object['properties']['Attributes']['HasToilet'])
                venue['has_wifi'] = str_to_boolean(geo_object['properties']['Attributes']['HasWifi'])
                venue['has_cash_machine'] = str_to_boolean(geo_object['properties']['Attributes']['HasCashMachine'])
                venue['has_first_aid'] = str_to_boolean(geo_object['properties']['Attributes']['HasFirstAidPost'])
                venue['has_equipment_rental'] = str_to_boolean(geo_object['properties']['Attributes']['HasEquipmentRental'])
                venue['equipment_rental_comments'] = geo_object['properties']['Attributes']['EquipmentRentalComments']
                venue['has_music'] = str_to_boolean(geo_object['properties']['Attributes']['HasMusic'])
                venue['disability_friendly'] = geo_object['properties']['Attributes']['DisabilityFriendly']
                venue['lighting'] = geo_object['properties']['Attributes']['Lighting']
                venue['paid'] = geo_object['properties']['Attributes']['Paid']
                venue['has_light'] = lighting_translate(geo_object['properties']['Attributes']['Paid'])
                if venue['paid'] == ('платно'):
                    venue['is_paid'] = True
                elif venue['paid'] == ('бесплатно'):
                    venue['is_paid'] = False
                venue['paid_comments'] = geo_object['properties']['Attributes']['PaidComments']
                venue['lat'] = geo_object['geometry']['coordinates'][1]
                venue['lon'] = geo_object['geometry']['coordinates'][0]
                venue['geo_data'] = geo_object['geometry']
                print(geo_object['properties']['Attributes']['global_id'])
                new_geo_object = GeoObject(**venue)
                new_geo_object.save()

                _geo_object = GeoObject.objects.get(global_id=venue['global_id'])

                if 'PhotoWinter' in geo_object['properties']['Attributes']:
                    #у нас зимняя фотография
                    photos = geo_object['properties']['Attributes']['PhotoWinter']
                    season = 'W'
                    photos_in_base = list(Photo.objects.filter(geo_object=_geo_object).values_list('api_id',flat=True))
                    
                    for photo in photos:
                        if photo['Photo'] in photos_in_base:
                            
                            get_photo_from_api(photo['Photo'])
                        else:
                            new_photo = {}
                            new_photo['geo_object'] = _geo_object
                            new_photo['season'] = 'W'
                            new_photo['api_id'] = photo['Photo']
                            new_photo['photo'] = get_photo_from_api(photo['Photo'])

                            new_photo_obj = Photo(**new_photo)
                            new_photo_obj.save()

                if 'PhotoSummer' in geo_object['properties']['Attributes']:
                    #у нас зимняя фотография
                    photos = geo_object['properties']['Attributes']['PhotoWinter']
                    season = 'W'
                    photos_in_base = list(Photo.objects.filter(
                        geo_object=_geo_object).values_list('api_id', flat=True))

                    for photo in photos:
                        if photo['Photo'] in photos_in_base:

                            get_photo_from_api(photo['Photo'])
                        else:
                            new_photo = {}
                            new_photo['geo_object'] = _geo_object
                            new_photo['season'] = 'S'
                            new_photo['api_id'] = photo['Photo']
                            new_photo['photo'] = get_photo_from_api(
                                photo['Photo'])

                            new_photo_obj = Photo(**new_photo)
                            new_photo_obj.save()
