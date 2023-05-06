import os

from django.core.management.base import BaseCommand
from utils.helper.account_creation import save_superuser

class Command(BaseCommand):
    """
    Command that creates super user and test users
    """

    help = "Creates super user and test users"

    def handle(self, *args, **options):

        create_superuser = input("Create superuser? y/N ")
        if create_superuser == "y" or create_superuser == "Y":
            """
            Add another superuser here...
            """
            save_superuser("admin", "admin@gmail.com", "Password1234!")
            save_superuser("colinjianingxie", "colinjianingxie@gmail.com", "Password1234!")
