import scrapy
import datetime
from math import ceil
from securities_master.models import Symbol

class WikiSpider(scrapy.Spider):
    """
    Download and parse the Wikipedia list of S&P500
    Returns a list of tuples for to add to MySQL.
    """

    name = "wiki-spider"

    table_id = 'constituents'
    mapping = {
        'symbol': 'td[1]/a',
        'security': 'td[2]/a',
        'sector': 'td[4]',
        'sub-industry': 'td[5]',
        'location': 'td[6]/a',
        'date-added': 'td[7]',
    }

    def start_requests(self):
        self.now = datetime.datetime.utcnow()
        self.counter = 0 #for debugging purposes

        urls = ['http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'] #list of all urls

        for link in urls:
            yield scrapy.Request(url = link, callback = self.parse)

    def parse(self, response):
        self.get_symbol_data(response)

    def get_symbol_data(self, response):
        '''
        Iterates through all of the table tr and inserts into django db
        '''
        for tr in response.xpath(f"//table[@id='{self.table_id}']/tbody/tr"):
            symbol = self.row_extract(tr, 'symbol')
            symbol = symbol[0] if len(symbol) > 0 else None

            security = self.row_extract(tr, 'security')
            security = security[0] if len(security) > 0 else None

            sector = self.row_extract(tr, 'sector')
            sector = sector[0] if len(sector) > 0 else None

            self.save_obj(
                symbol=symbol,
                stock_type='stock',
                exchange=None,
                security=security,
                sector=sector,
                currency='USD',
                created_date=self.now,
                updated_date=self.now)


    def row_extract(self, selector, data_type='symbol'):
        '''
        Extracts td from tr
        '''
        return selector.xpath(f"{self.mapping[data_type]}//text()").extract()

    def save_obj(self, symbol, stock_type, exchange, security, sector, currency, created_date, updated_date):

        if symbol:
            obj, created = Symbol.objects.get_or_create(
                ticker=symbol,
                exchange=exchange,
                instrument=stock_type,
                name=security,
                sector=sector,
                currency=currency,
                defaults={'created_date': created_date, 'last_updated_date': updated_date},
            )
            obj.save()
