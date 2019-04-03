from django.shortcuts import render


def events_map(request):
    return render(request, 'eventsapp/events_map.html')


def event(request, pk):
    return render(request, 'eventsapp/event.html')
