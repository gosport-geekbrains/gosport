from django.urls import path

import eventsapp.views as eventsapp_views

app_name = 'eventsapp'

urlpatterns = [
    path('', eventsapp_views.events_map, name='events_map'),
    path('<int:pk>/', eventsapp_views.event, name='event'),
    path('add/', eventsapp_views.add_event, name='add_event'),
]
