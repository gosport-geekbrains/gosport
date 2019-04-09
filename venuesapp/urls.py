from django.urls import path

import venuesapp.views as venuesapp_views

app_name = 'venuesapp'

urlpatterns = [
    path('', venuesapp_views.venues_map, name='venues_map'),
    path('<int:pk>/', venuesapp_views.venue, name='venue'),
    path('add/', venuesapp_views.add_venue, name='add_venue'),
    path('js/objects_manager.js', venuesapp_views.get_map_objects, name='create_yamap_js')

]
