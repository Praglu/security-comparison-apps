from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=128, blank=False, null=False)
    account_number = models.CharField(max_length=32, blank=False, null=False)
    amount = models.CharField(max_length=32, blank=False, null=False)
    reciever_info = models.CharField(max_length=128, blank=False, null=False)
    date = models.DateField(default=now, editable=True, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.date}_{self.title[:10]}'
