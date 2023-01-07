import uuid
from django.db import models

class Exchange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    abbrev = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=64, blank=True, null=True)
    timezone_offset = models.TimeField(blank=True, null=True)
    created_date = models.DateTimeField("created date", auto_now_add=True)
    last_updated_date = models.DateTimeField("last updated date", auto_now=True)

    def __str__(self):
        return f"{self.abbrev}"
