from django.db import models

from accounts.models import User


class APIKeyPair(models.Model):
    user = models.ForeignKey(User)
    keyID = models.IntegerField()
    vCode = models.CharField(max_length=64)

    def __str__(self):
        return self.keyID
