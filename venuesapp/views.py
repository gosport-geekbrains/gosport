from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from venuesapp.models import Category, Dataset, GeoObject, Photo, AdmArea, District
import os, json, requests

JSON_PATH = 'venuesapp/json'

def venues_map(request):
    content = {'yandex_api_key': settings.YANDEX_MAP_API_KEY,
                'adm_areas': AdmArea.objects.filter(is_active=True).order_by('name'),
                'districts': District.objects.filter(is_active=True).order_by('name')}
    return render(request, 'venuesapp/venues_map.html', content)


def venue(request, pk):

    venue = get_object_or_404(GeoObject, is_active=True, global_id=pk)
    try:
        venue_photos = Photo.objects.filter(is_active=True, geo_object_id=pk)
    except:
        venue_photos = {}

    content = {'title': venue.object_name,
               'venue': venue,
                'venue_photos': venue_photos,
                'yandex_api_key': settings.YANDEX_MAP_API_KEY}
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

#translate text values (yes or no) to boolean
def str_to_boolean(str):
    if str == 'да':
        return True
    else:
        return False

#translate text values to boolean for lighting type
def lighting_translate(str):
    nolight_str = "без дополнительного освещения"
    if str == nolight_str:
        return False
    else:
        return True

#get photo from original site
def get_photo_from_api(filename):
   
    url = settings.MOS_API_IMG_SRC.format(filename)
    result_file_path = os.path.join(
        settings.DOWNLOADED_PHOTO_PATH, filename+'.jpg')

    if os.path.exists(result_file_path) == False:
       
        response = requests.get(url)
        if response.status_code == 200:
            with open(result_file_path, 'wb') as imgfile:
                imgfile.write(response.content)
        #print(result_file_path, " downloaded")
    else:
        #print(result_file_path, " exists")
        pass
    return settings.MEDIA_PHOTO_PATH+filename+'.jpg'


def add_venue(request):
    return render(request, 'venuesapp/add_venue.html')

#
def get_map_objects(request):
    
    datasets = Category.objects.filter(is_active=True)
    adm_areas = AdmArea.objects.filter(is_active=True)
    districts = District.objects.filter(is_active=True)
    content = {
        'datasets': datasets,
        'adm_areas': adm_areas,
        'districts': districts,
        'venues_json': settings.VENUES_JSON_FILE
    }

    return render(request, 'venuesapp/js/objects_manager.js', content)


def get_map_object(request, pk):
    pass

