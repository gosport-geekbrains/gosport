from django.urls import path

from mainapp import views as mainapp_views

urlpatterns = [
    path('', mainapp_views.index, name='index'),
]
