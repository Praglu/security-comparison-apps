from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect


def login_function(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request=request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/user/user-info')
    return HttpResponse(status=401)


def logout_function(request):
    logout(request)
    return redirect('/')
