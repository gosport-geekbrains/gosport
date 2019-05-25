from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from venuesapp.models import Category, Dataset, GeoObject, Photo, AdmArea, District, get_objects_in_bounds
import os, json, requests
from PIL import Image
from pathlib import Path

JSON_PATH = 'venuesapp/json'

def venues_map(request):
    content = {'yandex_api_key': settings.YANDEX_MAP_API_KEY,
                'adm_areas': AdmArea.objects.filter(is_active=True).order_by('name'),
                #'districts': District.objects.filter(is_active=True).order_by('name'),
                'categories': Category.objects.filter(is_active=True).order_by('name')
                }
    return render(request, 'venuesapp/venues_map.html', content)


def venue(request, pk):

    venue = get_object_or_404(GeoObject, is_active=True, pk=pk)
    try:
        venue_photos = Photo.objects.filter(is_active=True, geo_object__pk=pk)

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
    categories = Category.objects.filter(is_active=True)
    content = {
        'categories': categories,
        'adm_areas': adm_areas,
        'venues_json': settings.VENUES_JSON_FILE
    }

    return render(request, 'venuesapp/js/objects_manager.js', content)



def get_objects_in(request):
    bounds = []
    bounds = json.loads(request.POST['bounds'])
    #print(request.POST.get('filter'))
    filter = json.loads(request.POST.get('filter'))
    #print(filter)
    if request.is_ajax():
        venues = get_objects_in_bounds(bounds, filter=filter)
        result = []
        for venue in venues:
            try:
                venue_photo = Photo.objects.filter(
                    is_active=True, geo_object__pk=venue[0]).latest('pk')
                photo = f'/media{settings.MEDIA_THUMB_PATH}{venue_photo.api_id}.jpg'
                #thumb_photo = f'{settings.MEDIA_THUMB_PATH}{venue_photo.photo.api_id}'
            except Photo.DoesNotExist:
                photo = settings.VENUE_NO_PHOTO_IMAGE
                thumb_photo = settings.VENUE_NO_PHOTO_IMAGE

            venue = get_object_or_404(GeoObject, pk=venue[0])

            result.append({
                'pk': venue.pk,
                'name': venue.get_name(), 
                'description': venue.description,
                'paid': venue.paid, 
                'category': venue.object_type.name,
                'light': venue.lighting,
                'photo': photo,
                #'thumb': thumb_photo
                })    

        #print(result)

        return JsonResponse(json.dumps(result,  ensure_ascii=False), safe=False)

    return JsonResponse({'data': 0})


def create_preview(filename):

    img_path = os.path.join(settings.DOWNLOADED_PHOTO_PATH, f'{filename}.jpg')

    if os.path.exists(img_path):

        thumb_path = os.path.join(settings.PHOTO_THUMB_PATH, f'{filename}.jpg')

        if os.path.exists(thumb_path):
            return True

        #imgfile = Path(filename)
        img = Image.open(img_path)

        #определим соотношеине сторон, если фотография вертикальная - вырезать кусок из центра в соотношении 3х4
        width = img.size[0]
        height = img.size[1]
        #img3 = img.crop((0, 0, width, height-20))

        if height >= width:
            height_new = width * 3/4
            params = (0, (height/2)-height_new/2, width, (height/2)+height_new/2)

        elif width*3/4 != height:
            width_new = height * 4/3
            params = (0, 0, width_new, height)

        else:
            params = (0, 0, width, height)

        img_new = img.crop(params)
        img_new.save(thumb_path, format="JPEG", quality=70)
        img.close
        return True
    else:
        return False
