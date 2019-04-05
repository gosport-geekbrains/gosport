from django.shortcuts import render


def venues_map(request):
    return render(request, 'venuesapp/venues_map.html')


def venue(request, pk):
    return render(request, 'venuesapp/venue.html')


def add_venue(request):
    return render(request, 'venuesapp/add_venue.html')
