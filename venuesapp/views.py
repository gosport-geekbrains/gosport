from django.shortcuts import render


def venues_map(request):
    return render(request, 'venuesapp/venues_map.html')


def venue(request, pk):
    return render(request, 'venuesapp/venue.html')
