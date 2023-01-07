import os

from django.core.management.base import BaseCommand
from main.pricing import perform_adf, perform_hurst, perform_cadf, perform_confusion_matrix, perform_sharpe, perform_var

class Command(BaseCommand):
    """
    Command that performs adf on ticker symbol
    """

    help = ""

    def add_arguments(self, parser):
        parser.add_argument('-n', type=str, help='analysis name: adf, ')


    def handle(self, *args, **options):
        analysis_name = options['n']

        if analysis_name == "adf":
            perform_adf()
        elif analysis_name == "hurst":
            perform_hurst()
        elif analysis_name == "cadf":
            perform_cadf()
        elif analysis_name == "cm":
            perform_confusion_matrix()
        elif analysis_name == "sharpe":
            perform_sharpe()
        elif analysis_name == "var":
            perform_var()
