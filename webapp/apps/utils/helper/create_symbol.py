from securities_master.models import Symbol
import datetime

def create_symbol():
    ticker_name = input("Enter ticker name: ")
    #instrument = input("Enter instrument (stock, fx): ")
    name = input("Enter name of security: ")
    stock_type = input("Enter equity type: ")
    sector = input("Enter sector: ")
    #currency = input("Enter currency: ")
    now = datetime.datetime.utcnow()
    save_obj(
        symbol=ticker_name,
        stock_type=stock_type,
        exchange=None,
        security=name,
        sector=sector,
        currency='USD',
        created_date=now,
        updated_date=now)

def save_obj(symbol, stock_type, exchange, security, sector, currency, created_date, updated_date):

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
