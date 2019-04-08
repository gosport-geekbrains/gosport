from django.shortcuts import render


def index(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def thank_you(request):
    return render(request, 'mainapp/thank_you.html')
