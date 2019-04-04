from django.shortcuts import render
from django.conf import settings

import os, json, requests

JSON_PATH = 'venuesapp/json'

def venues_map(request):
    return render(request, 'venuesapp/venues_map.html')


def venue(request, pk):
    return render(request, 'venuesapp/venue.html')

    
#DB Initialization 

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as f:
        return json.load(f)


def get_json_from_api(dataset_id, str_features='all'):
    url = 'https://apidata.mos.ru/v1/datasets/{}/features/?api_key={}'.format(dataset_id, settings.MOS_API_KEY)
    print(dataset_id, str_features)
    req = requests.post(url, json=str_features)
    #print(req.status_code)
    str = req.content.decode('utf8')
    print(str)
    return json.loads(str)
