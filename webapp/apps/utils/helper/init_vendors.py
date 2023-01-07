from datetime import datetime as dt
from securities_master.models import DataVendor

VENDOR_MAPPING = {
	'AlphaVantage': {
		'website_url': "https://alphavantage.co/",
		'support_email': "support@alphavantage.co"
	},
	'Yahoo Finance': {
		'website_url': "https://github.com/ranaroussi/yfinance",
		'support_email': "https://github.com/ranaroussi/yfinance"
	}
}

def create_or_update_vendor(vendor_name):
	curr = dt.utcnow()

	try:
		av_obj = DataVendor.objects.get(
			name=vendor_name,
		)
		av_obj.last_updated_date = curr
		av_obj.save()
		return av_obj
	except DataVendor.DoesNotExist:
		av_obj = DataVendor(
			name=vendor_name,
			website_url=VENDOR_MAPPING[vendor_name]['website_url'],
			support_email=VENDOR_MAPPING[vendor_name]['support_email'],
			created_date=curr,
			last_updated_date=curr)
		av_obj.save()
		return av_obj
