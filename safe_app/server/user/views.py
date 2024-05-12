from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from server.transfer.models import Transfer
from server.official.models import Official



def index(request):
    return render(request, 'user/index.html', {})


def user_info(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        transfers = Transfer.objects.filter(user=user)
        officials = Official.objects.filter(user=user)
        return render(
            request,
            'user/user-info.html',
            {
                'user': user,
                'transfers': transfers,
                'officials': officials,
            },
        )
    return HttpResponse(status=401)


def create_user(request):
    username = request.POST['username']
    email = f'{username}@testdjangoapp.com'
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return render(request, 'user/created-user.html', {'user': user})
    except:
        return HttpResponse(status=400)


def sign_up(request):
    return render(request, 'user/sign-up.html', {})
