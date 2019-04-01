from django.shortcuts import render


def login(request):
    return render(request, 'authapp/login.html')


def logout(request):
    pass


def register(request):
    return render(request, 'authapp/register.html')


def profile(request):
    return render(request, 'authapp/profile.html')
