from django.http import HttpResponse
from django.shortcuts import render

from server.transfer.models import Transfer


def create_transfer(request):
    return render(request, 'user/create-transfer.html', {})


def post_transfer(request):
    title = request.POST['title']
    account_number = request.POST['account_number']
    amount = request.POST['amount']
    reciever_info = request.POST['reciever_info']
    date = request.POST['date']

    try:
        transfer = Transfer.objects.create(
            user=request.user,
            title=title,
            account_number=account_number,
            amount=amount,
            reciever_info=reciever_info,
            date=date,
        )
        return render(request, 'user/successful-transfer.html', {'transfer': transfer})
    except Exception as e:
        return HttpResponse(status=400, reason=e)
