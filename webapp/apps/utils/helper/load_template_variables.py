from securities_master.models import Symbol

def load_all_symbols(request):
    symbols = Symbol.objects.all().order_by('ticker')
    return {'symbols': symbols}
