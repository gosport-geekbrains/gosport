from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        context = {
            'username': username,
            'password': password
        }

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('auth:user_dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return render(request, 'authapp/login.html', context)

    return render(request, 'authapp/login.html')


def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        # Get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        context = {
            'username': username,
            'email': email,
            'password': password,
            'password2': password2
        }

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким логином уже существует')
                return render(request, 'authapp/register.html', context)
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Указанный электронный адрес уже используется')
                    return render(request, 'authapp/register.html', context)
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                    )
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'Ваш пользователь успешно создан!', )
                    return redirect('auth:login')
        else:
            messages.error(request, 'Подтвержение не совпадает с паролем')
            return render(request, 'authapp/register.html', context)

    return render(request, 'authapp/register.html')


@login_required()
def profile(request):
    return render(request, 'authapp/profile.html')


@login_required()
def dashboard(request):
    return render(request, 'authapp/dashboard.html')
