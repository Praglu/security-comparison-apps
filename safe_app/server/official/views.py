from django.http import HttpResponse
from django.shortcuts import render

from server.official.models import Official


def create_official(request):
    return render(request, 'user/create-official.html', {})


def post_official(request):
    description = request.POST['description']
    date = request.POST['date']

    try:
        Official.objects.create(
            user=request.user,
            description=description,
            date=date,
        )
        return render(request, 'user/successful-official.html', {})
    except:
        return HttpResponse(status=400)
