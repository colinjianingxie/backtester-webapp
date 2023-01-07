from django.core.management.base import BaseCommand
from utils.helper.create_symbol import create_symbol as cs


class Command(BaseCommand):
    """
    Command that saves custom symbol.
    """

    help = "Create custom symbol"

    def handle(self, *args, **options):
        cs()
