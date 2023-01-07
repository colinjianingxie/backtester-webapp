import os

from django.core.management.base import BaseCommand
import datetime
from math import ceil
from utils.vendors.alphavantage.price_retrieval import start_alphavantage
from utils.vendors.yfinance.price_retrieval import start_yahoo_finance

class Command(BaseCommand):
    """
    Command that scrapes S&P 500 companies from wikipedia.
    """

    help = "Scrapes S&P 500 from wiki"

    def handle(self, *args, **options):
        #start_alphavantage()
        start_yahoo_finance()
