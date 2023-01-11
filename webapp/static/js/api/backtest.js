
$("#perform-backtest").click(function() {
    const start_date = $("#backtest-data-start-date").val()
    const end_date = $("#backtest-data-end-date").val()
    const portfolio_start_date = $("#backtest-portfolio-start-date").val()

    const name="Test_bt2"
    const ticker = $('#stock-label-0').data('ticker');
    const symbol_list=[ticker]
    const initial_capital= $('#initial-backtest-value').data('initial-capital')
    const heartbeat=0.0
    const data_handler="HistoricDataHandler"
    const execution_handler="SimulatedExecutionHandler"
    const portfolio="Portfolio"
    //const strategy="SPYDailyForecastStrategy"
    const strategy= $("#backtest-strategy-selected").data('strategy')

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
        strategy_parameters: JSON.stringify(exampleStrategyObj[strategy]['parameters']),
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
    // Refreshes stock picker...
    const ticker = $(this).data('ticker');
    var options = {
      api: urls.backtest_daily_price,
      body: {
        ticker: ticker,
      },
      complete_function: closeBacktestStockPickerModal,
    }

    post_request_template(options, "#backtest-stock-selection")

    updateDailyPriceChart('../..', ticker, backtestPriceChart)
});

$(".selectStrategy").click(function() {
    const strategy = $(this).data('strategy');
    $('.strategySelectModal').modal('hide');
    $("#backtest-strategy-selected").html(strategy);
    $("#backtest-strategy-selected").data('strategy', strategy);

    // Make API call to obtain strategy parameters...
    var options = {
      api: urls.post_backtest_strategy_parameter,
      body: {
        strategy: strategy,
      },
      complete_function: closeBacktestParameterModal,
    }
    post_request_template(options, "#strategy-parameter-body")

});
