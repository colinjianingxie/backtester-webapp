import os

from django.core.management.base import BaseCommand
from utils.helper.account_creation import save_superuser

class Command(BaseCommand):
    """
    Command that creates super user and test users
    """

    help = "Creates super user and test users"

    def handle(self, *args, **options):

        #create_superuser = input("Create superuser? y/N ")
        create_superuser = "y"
        if create_superuser == "y" or create_superuser == "Y":
            save_superuser("colinjianingxie", "colinjianingxie@gmail.com", "Password1234!")
            save_superuser("calvinxie", "calvinjxie@gmail.com", "Password1234!")
