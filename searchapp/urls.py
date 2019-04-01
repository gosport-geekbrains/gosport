from django.urls import path

import searchapp.views as searchapp_views

app_name = 'searchapp'

urlpatterns = [
    path('venues/', searchapp_views.search_venues, name='search_venues'),
    path('events/', searchapp_views.search_events, name='search_events'),
]
