from securities_master.models import DailyPrice
from securities_master.models import Symbol

def load_all_symbols(request):

    daily_price_id = [dpid['symbol_id'] for dpid in DailyPrice.objects.values('symbol_id').distinct()]
    symbols = Symbol.objects.filter(id__in=daily_price_id)
    return {'symbols': symbols}
