from main.models import Strategy
from oauth.models import Account

DEFAULT_STRATEGIES = {
	'MovingAverageCrossover': {
		'description': 'Carries out a basic Moving Average Crossover strategy with a short or long simple \
						weighted moving average. Default short/long windows are 100 or 400 periods \
						respectively.',
		'parameters': {
			'long_window': 'number',
			'short_window': 'number',
		},
		'defaults': {
			'long_window': 400,
			'short_window': 100,
		},
		'min': {
			'long_window': 300,
			'short_window': 10,
		},
		'max': {
			'long_window': 800,
			'short_window': 300,
		},
		'use_ml': False,
	},
	'MLForecast': {
		'description': 'This model uses a Quadratic Discriminant Analyser to predict \
						the returns for a subsequent time period and then generated long or \
						exit signals based on the prediction.',
		'parameters': {
			'model_start_date': 'date',
			'model_end_date': 'date',
			'model_start_test_date': 'date',
		},
		'defaults': {
			'model_start_date': '2016-01-10',
			'model_end_date': '2017-12-31',
			'model_start_test_date': '2017-01-01'
		},
		'min': {},
		'max': {},
		'use_ml': True,
	}
}


def get_builtin(name):
	return getattr(__builtins__, name)


def create_or_update_default_strategies():
	'''
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	strategy_parameters = JSONField(default={})
	use_ml = models.BooleanField(default=False)
	'''
	curr_acc = Account.objects.all().filter(username='colinjianingxie').first()
	for name, value in DEFAULT_STRATEGIES.items():
		try:
			strat = Strategy.objects.get(
				account=curr_acc,
				name=name,
				description=value['description'],
				strategy_parameters=value['parameters'],
				strategy_defaults=value['defaults'],
				strategy_min=value['min'],
				strategy_max=value['max'],
				use_ml=value['use_ml'])
		except Strategy.DoesNotExist:
			strat = Strategy(
				account=curr_acc,
				name=name,
				description=value['description'],
				strategy_parameters=value['parameters'],
				strategy_defaults=value['defaults'],
				strategy_min=value['min'],
				strategy_max=value['max'],
				use_ml=value['use_ml'])
			strat.save()
