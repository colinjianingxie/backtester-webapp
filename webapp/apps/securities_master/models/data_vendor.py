import uuid
from django.db import models

class DataVendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    support_email = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField("created date", auto_now_add=True)
    last_updated_date = models.DateTimeField("last updated date", auto_now=True)

    def __str__(self):
        return f"{self.name}"
