from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from venuesapp.models import Category, Dataset, GeoObject, Photo
import os, json, requests

JSON_PATH = 'venuesapp/json'

def venues_map(request):
    content = {'yandex_api_key': settings.YANDEX_MAP_API_KEY}
    return render(request, 'venuesapp/venues_map.html', content)


def venue(request, pk):

    venue = get_object_or_404(GeoObject, is_active=True, global_id=pk)
    try:
        venue_photos = Photo.objects.filter(is_active=True, geo_object_id=pk)
    except:
        venue_photos = {}

    content = {'title': venue.object_name,
               'venue': venue,
                'venue_photos': venue_photos }
    return render(request, 'venuesapp/venue.html', content)

    
#DB Initialization 

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_json_from_api(dataset_id, str_features):
    url = 'https://apidata.mos.ru/v1/datasets/{}/features/?api_key={}'.format(dataset_id, settings.MOS_API_KEY)
    req = requests.post(url, json=str_features)
    #print(req.status_code)
    str = req.content.decode('utf8')
    
    return json.loads(str)

def str_to_boolean(str):
    if str == 'да':
        return True
    else:
        return False

def get_photo_from_api(filename):
   
   url = settings.MOS_API_IMG_SRC.format(filename)
   result_file_path = settings.MOS_API_IMG_PATH+"\\"+filename+'.jpg'

   if os.path.exists(result_file_path) == False:
       
       response = requests.get(url)
       if response.status_code == 200:
            with open(result_file_path, 'wb') as imgfile:
                imgfile.write(response.content)
       print(result_file_path, " downloaded")
   else:
       print(result_file_path, " exists")
   return settings.PHOTOS_PATH + '/' + filename+'.jpg'

def get_season():
        #сверить дату с usage для определения того, какие данные выдавать - летние или зимние
        pass

def add_venue(request):
    return render(request, 'venuesapp/add_venue.html')

def get_map_objects(request):

    datasets = Category.objects.filter(is_active=True)
    content = {
        'datasets': datasets
    }

    return render(request, 'venuesapp/js/objects_manager.js', content)

