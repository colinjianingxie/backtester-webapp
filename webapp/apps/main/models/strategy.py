import json
import uuid

from django.db import models
from jsonfield import JSONField
from oauth.models import Account

class Strategy(models.Model):
    """
    test
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    strategy_parameters = JSONField(default={})
    strategy_defaults = JSONField(default={})
    strategy_min = JSONField(default={})
    strategy_max = JSONField(default={})
    use_ml = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id}"
