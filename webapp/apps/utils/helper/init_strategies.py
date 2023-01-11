from main.models import Strategy
from oauth.models import Account

DEFAULT_STRATEGIES = {
	'MovingAverageCrossover': {
		'description': 'Carries out a basic Moving Average Crossover strategy with a short or long simple \
						weighted moving average. Default short/long windows are 100 or 400 periods \
						respectively.',
		'parameters': {
			'long_window': 'int',
			'short_window': 'int',
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
				use_ml=value['use_ml'])
		except Strategy.DoesNotExist:
			strat = Strategy(
				account=curr_acc,
				name=name,
				description=value['description'],
				strategy_parameters=value['parameters'],
				use_ml=value['use_ml'])
			strat.save()
