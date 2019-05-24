from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.conf import settings


#from venuesapp.models import CategoryClear
from venuesapp.models import Photo




class Command(BaseCommand):
    help = 'create thumbs'

    def add_arguments(self, parser):
        parser.add_argument('--clear',
                            action='remove_all',
                            help='clear all thumbs')

    def handle(self, *args, **options):
        pass
