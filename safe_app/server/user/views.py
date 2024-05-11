from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render



def index(request):
    return render(request, 'user/index.html', {})


def user_info(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        return render(request, 'user/user-info.html', {'user': user})
    return HttpResponse(status=401)
