import statsmodels.tsa.stattools as ts
from main.pricing.helpers.get_daily_prices import get_daily_prices
from main.pricing.helpers.basic_input import call_basic_security_input

def perform_adf():

    ticker_names, start_date, end_date = call_basic_security_input()

    lag_order = input("Lag order: ")
    lag_order = int(lag_order)

    daily_prices = get_daily_prices(ticker_names=ticker_names, start_date=start_date, end_date=end_date)

    # Output the results of the Augmented Dickey-Fuller test for Amazon
    # with a lag order value of 1
    print("---------")
    test_statistic, p_value, samples_run, sample_size, stats, x = ts.adfuller(daily_prices['adj_close_price'], lag_order)
    print(f"number samples: {sample_size}")
    print(f"test_statistic: {test_statistic}")
    print(f"p value: {p_value}")
    for key, value in stats.items():
        significant = "significant and POSSIBLY mean reverting" if test_statistic < value else "not significant and NOT mean reverting"
        print(f"critical at {key}: {value} ({significant})")
