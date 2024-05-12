from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Official(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=512, blank=False, null=False)
    date = models.DateField(default=now, editable=True, blank=False, null=False)

    def __str__(self) -> str:
        return f'{self.date}_{self.description[:15]}'
