import uuid

from django.db import models
from oauth.models import Account


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_constraint=False)

    def __name__(self):
        return "User model"

    def __str__(self):
        return f"{self.account}"


class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_constraint=False)

    def __name__(self):
        return "admin model"

    def __str__(self):
        return f"{self.account}"
