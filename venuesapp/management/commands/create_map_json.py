from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import requests
import json

#from venuesapp.models import CategoryClear
from venuesapp.models import Category, GeoObject, District, AdmArea, Photo, Dataset

#from venuesapp.views import load_from_json, get_json_from_api, str_to_boolean, get_photo_from_api

#JSON_PATH = 'venuesapp/json'


class Command(BaseCommand):
    help = 'create full JSON for Yamap'
    def add_arguments(self, parser):
        parser.add_argument('--detail',
                            action='store_true',
                            help='generating json with additonal info')


    def handle(self, *args, **options):

        geo_objects = GeoObject.objects.select_related().filter(is_active=True)


        geo_object_json = {}

        #with open(settings.YANDEX_JSON_FILE, 'w+', encoding='utf-8') as json_file:
        json_result = {}
        json_result['type'] = "FeatureCollection"
        json_result['features'] = []
        #json_file.write(' { "type" : "FeatureCollection", "features" : [')    
        for geo_object in geo_objects:
            geo_object_json = {}
            geo_object_json['type'] = "Feature"
            geo_object_json['id'] = geo_object.global_id
            geo_object_json['geometry'] = {
                'coordinates': [geo_object.lat, geo_object.lon], 
                'type': 'Point'
            }
            geo_object_json['properties'] = {
                'balloonContentHeader': geo_object.name_winter,
                'balloonContentBody': "<a href='/venues/{id}/'>{object_name}</a>".format(
                    object_name=geo_object.object_name, id=geo_object.global_id),
                'dataset_id': Dataset.objects.get(name=geo_object.object_type).dataset_id
                }
            if options['detail']:

                #print(AdmArea.objects.get(name=geo_object.adm_area).id)

                geo_object_json['properties'].update({
                    'adm_area': geo_object.adm_area_id,
                    'district': geo_object.district_id
                })

            geo_object_json['options'] = {'iconImageHref': '/static/images/map_markers/{}'.format(
                Category.objects.get(name=geo_object.object_type).marker),
                'preset': Category.objects.get(name=geo_object.object_type).ya_preset}
            #print(geo_object_json)
            json_result['features'].append(geo_object_json)
        #    json_file.write(json.dumps(geo_object_json, ensure_ascii=False))
        #json_file.write('}')
        #print(json_result)
        
        with open(settings.YANDEX_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, ensure_ascii=False)
            #f.write(str(json_result))
            #pass
