from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.conf import settings
from venuesapp.views import create_preview


#from venuesapp.models import CategoryClear
from venuesapp.models import Photo
from venuesapp.views import create_preview




class Command(BaseCommand):
    help = 'create thumbs'

    def add_arguments(self, parser):
        parser.add_argument('--detail',
                            action='store_true',
                            help='generating json with additonal info')

    def handle(self, *args, **options):
        
        #print(create_preview('00ed0a5b-1151-470e-ae85-e8f7cecf8d55'))
        
        photos = Photo.objects.filter(is_active=True)

        for photo in photos:
            print(create_preview(photo.api_id))