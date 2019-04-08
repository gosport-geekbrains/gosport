from django.urls import path

from mainapp import views as mainapp_views

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp_views.index, name='index'),
    path('contact/', mainapp_views.contact, name='contact'),
    path('thank_you/', mainapp_views.thank_you, name='thank_you'),
]
