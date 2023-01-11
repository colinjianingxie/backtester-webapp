import os

from django.core.management.base import BaseCommand
from utils.helper.init_strategies import create_or_update_default_strategies
class Command(BaseCommand):
    """
    Command that initializes the db by adding migration files, migrating and creating the necessary groups.
    """

    help = "Initializes the database"

    def handle(self, *args, **options):
        os.system("python3 manage.py scrape_wiki")
        os.system("python3 manage.py scrape_vendors")
        create_or_update_default_strategies()
