import os

from django.core.management.base import BaseCommand
from securities_master.models import DataVendor, Exchange
class Command(BaseCommand):
    """
    Command that initializes the db by adding migration files, migrating and creating the necessary groups.
    """

    help = "Initializes the database"

    def handle(self, *args, **options):
        pass
