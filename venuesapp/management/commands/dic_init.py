from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
import json

#from venuesapp.models import CategoryClear
from venuesapp.models import Category, GeoObject, District, AdmArea, Photo, Dataset

from venuesapp.views import load_from_json, get_json_from_api, str_to_boolean, get_photo_from_api

JSON_PATH = 'venuesapp/json'

STR_FEATURES = '[]'

MAP_JS_PATH = '\static\json'




class Command(BaseCommand):
    help = 'Fill DB new data'

    def handle(self, *args, **options):

        datasets = load_from_json('datasets')
        Dataset.objects.all().delete()
        Category.objects.all().delete()
        GeoObject.objects.all().delete()
        Photo.objects.all().delete()

        for dataset in datasets:

            new_dataset = Dataset(**dataset)
            new_dataset.save()
            
            new_category = Category(**dataset)
            new_category.save()

            #dataset['dataset_id'] = "886"

            geo_objects = get_json_from_api(dataset['dataset_id'], STR_FEATURES)

            #with open(dataset['dataset_id']+'.json', 'w', encoding='utf-8') as f:
            #    json.dump(geo_objects, f, ensure_ascii=False)
           

            for geo_object in geo_objects['features']:
                venue = {}

                #test of admArea dict
                try:
                    venue['adm_area'] = AdmArea.objects.get(
                        name=geo_object['properties']['Attributes']['AdmArea'])
                except:
                    new_adm_area = AdmArea(
                        name=geo_object['properties']['Attributes']['AdmArea'])
                    new_adm_area.save()
                    venue['adm_area'] = AdmArea.objects.get(
                        name=geo_object['properties']['Attributes']['AdmArea'])
               
                #test of Dstrict dict
                try:
                    venue['district'] = District.objects.get(
                        name=geo_object['properties']['Attributes']['District'])
                except:
                    new_district = District(
                        name=geo_object['properties']['Attributes']['District'])
                    new_district.save()
                    venue['district'] = District.objects.get(
                        name=geo_object['properties']['Attributes']['District'])

                venue['global_id'] = geo_object['properties']['Attributes']['global_id']
                
                _category_type = Category.objects.get(name=dataset['name'])
                venue['object_type'] = _category_type
                venue['object_name'] = geo_object['properties']['Attributes']['ObjectName']
                
                if 'NameWinter' in geo_object['properties']['Attributes']:
                    venue['name_winter'] = geo_object['properties']['Attributes']['NameWinter']
                    venue['working_hours_winter'] = geo_object['properties']['Attributes']['WorkingHoursWinter']
                    venue['services_winter'] = geo_object['properties']['Attributes']['ServicesWinter']
                    venue['surface_type_winter'] = geo_object['properties']['Attributes']['SurfaceTypeWinter']
                    venue['usage_period_winter'] = geo_object['properties']['Attributes']['UsagePeriodWinter']

                

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
                venue['paid_comments'] = geo_object['properties']['Attributes']['PaidComments']
                venue['lat'] = geo_object['geometry']['coordinates'][1]
                venue['lon'] = geo_object['geometry']['coordinates'][0]
                venue['geo_data'] = geo_object['geometry']
                print(geo_object['properties']['Attributes']['global_id'])
                new_geo_object = GeoObject(**venue)
                new_geo_object.save()

                 
                try:
                    new_photo = {}
                    #нужна проверка наличия файла в папке перед скачкой

                    new_photo['photo'] = get_photo_from_api(
                        geo_object['properties']['Attributes']['PhotoWinter'][0]['Photo'])
                    _geo_object = GeoObject.objects.get(global_id=venue['global_id'])
                    
                    new_photo['geo_object'] = _geo_object
                    
                    photo = Photo(**new_photo)
                    photo.save()
                except:
                    pass
                
