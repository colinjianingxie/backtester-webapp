from securities_master.models import Exchange
from datetime import datetime as dt

VENDOR_MAPPING = {
	'S&P 500': {
		'abbreviation': "https://alphavantage.co/",
		'name': "support@alphavantage.co",
        'city': "support@alphavantage.co",
        'country': "United States of America",
        'currency': "USD",
        'timezone_offset': "support@alphavantage.co",
	}
}


def create_or_update_exchange(exchange_name):
	curr = dt.utcnow()
    pass
