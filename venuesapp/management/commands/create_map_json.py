from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
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
            #print(geo_object.global_id,' ', geo_object.get_current_season())
            #print(geo_object.global_id,  ' ', geo_object.get_working_hours())
            geo_object_json = {}
            geo_object_json['type'] = "Feature"
            geo_object_json['id'] = geo_object.pk
            geo_object_json['geometry'] = {
                'coordinates': [round(geo_object.lat,6), round(geo_object.lon,6)], 
                'type': 'Point'
            }
            geo_object_json['properties'] = {
                'balloonContentHeader': "<a href='/venues/{id}/'>{object_name}</a>".format(
                    object_name=geo_object.object_name, id=geo_object.pk),
                #'balloonContentBody': "<a href='/venues/{id}/'>{object_name}</a>".format(
                #    object_name=geo_object.object_name, id=geo_object.global_id),
                'dataset_id': Dataset.objects.get(name=geo_object.object_type).dataset_id
                }

            geo_object_json['properties'].update({
                'adm': '{}'.format(geo_object.adm_area_id),
                'dist': '{}'.format(geo_object.district_id),
                'light': '{:d}'.format(geo_object.has_light),
                'toilet': '{:d}'.format(geo_object.has_toilet),
                'eat': '{:d}'.format(geo_object.has_eatery),
                'dress': '{:d}'.format(geo_object.has_dressing)

            })

            if options['detail']:
                pass
                #print(AdmArea.objects.get(name=geo_object.adm_area).id)


            geo_object_json['options'] = {
            # 'iconImageHref': '/static/images/map_markers/{}'.format(
            #    Category.objects.get(name=geo_object.object_type).marker),
                'preset': Category.objects.get(name=geo_object.object_type).ya_preset
            }
            #print(geo_object_json)
            json_result['features'].append(geo_object_json)
        #    json_file.write(json.dumps(geo_object_json, ensure_ascii=False))
        #json_file.write('}')
        #print(json_result)
        
        with open(settings.VENUES_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, ensure_ascii=False)
            #f.write(str(json_result))
            #pass
