import os

from django.core.management.base import BaseCommand
import datetime
from math import ceil
from scrapy.crawler import CrawlerProcess
from securities_scraper.main.spiders.wiki_spider import WikiSpider



class Command(BaseCommand):
    """
    Command that scrapes S&P 500 companies from wikipedia.
    """

    help = "Scrapes S&P 500 from wiki"

    def handle(self, *args, **options):
        process = CrawlerProcess()
        process.crawl(WikiSpider)
        process.start()
