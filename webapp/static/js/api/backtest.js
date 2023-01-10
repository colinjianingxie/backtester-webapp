function go_to_result(response_data) {
  window.location.href = `../../${urls.backtest_result}/${response_data.backtest_id}/${response_data.backtest_result_id}`;
}

function closeBacktestStockPickerModal() {
  $('.backtestStockPickerModal').modal('hide');

}

$("#perform-backtest").click(function() {
    const start_date = '1998-01-02'
    const end_date = '2018-01-31'
    const portfolio_start_date = '2017-01-03'

    const strat_a = {
            'short_window': 100,
            'long_window': 400,
    }

    const strat_b = {
      'start_date': '2016-01-10',
      'end_date': '2017-12-31',
      'start_test_date': '2017-01-01',
    }


    const name="Test_bt2"
    const ticker = $('#stock-label-0').data('ticker');
    const symbol_list=[ticker]
    const initial_capital=100000.00
    const heartbeat=0.0
    const data_handler="HistoricDataHandler"
    const execution_handler="SimulatedExecutionHandler"
    const portfolio="Portfolio"
    const strategy="SPYDailyForecastStrategy"
    //const strategy="MovingAverageCrossStrategy"

    var options = {
      api: urls.perform_backtest,
      body: {
        name: name,
        symbol_list: JSON.stringify(symbol_list),
        initial_capital: initial_capital,
        heartbeat: heartbeat,
        data_handler: data_handler,
        execution_handler: execution_handler,
        portfolio: portfolio,
        strategy: strategy,
        strategy_parameters: JSON.stringify(strat_b),
        data_start_date: start_date,
        data_end_date: end_date,
        portfolio_start_date: portfolio_start_date,
      },
      success_url: urls.backtest_result,
      data_function: go_to_result,
    }

    post_request(options)
});

$(".apply-backtest-daily-price").click(function() {
    const ticker = $(this).data('ticker');
    var options = {
      api: urls.backtest_daily_price,
      body: {
        ticker: ticker,
      },
      complete_function: closeBacktestStockPickerModal,
    }

    post_request_template(options, "#backtest-stock-selection")

    var chartOptions = {
        api: `../../${urls.get_daily_price_coordinates_json}/${ticker}`,
    }
    get_chart_json(chartOptions, testChart)
});
