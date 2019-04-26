from django.core.management.base import BaseCommand, CommandError

from venuesapp.models import GeoObject
from venuesapp.views import lighting_translate

class Command(BaseCommand):
    help = 'Fill boolean light field in DB'

    def handle(self, *args, **options):
        geo_objects = GeoObject.objects.all()

        for geo_object in geo_objects:
            geo_object.has_light = lighting_translate(geo_object.lighting)
            geo_object.save()
