
$("#perform-backtest").click(function() {
    const name="Test_bt2"
    const start_date = $("#backtest-data-start-date").val()
    const end_date = $("#backtest-data-end-date").val()
    const portfolio_start_date = $("#backtest-portfolio-start-date").val()
    const ticker = $('#stock-label-0').data('ticker');
    const symbol_list=[ticker]
    const initial_capital= $('#initial-backtest-value').data('initial-capital')
    const strategy= $("#backtest-strategy-selected").data('strategy')
    var strategy_parameters = {};
    const heartbeat=0.0
    const data_handler="HistoricDataHandler"
    const execution_handler="SimulatedExecutionHandler"
    const portfolio="Portfolio"

    const beforeText = 'Perform Backtest'
    const loaderText = '<i class="bx bx-loader bx-spin font-size-16 align-middle me-2"></i> Loading';
    // TODO: Can probably use javascript's REDUCE function...
    $("form#backtest-parameter-form :input").each(function(){
        var parameter_name = $(this).data('parameter-name');
        var parameter_value = $(this).val();
        strategy_parameters[parameter_name] = parameter_value;
    });

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
        strategy_parameters: JSON.stringify(strategy_parameters),
        data_start_date: start_date,
        data_end_date: end_date,
        portfolio_start_date: portfolio_start_date,
      },
      success_url: urls.backtest_result,
      data_function: go_to_result,
      complete_function: function(){$('#perform-backtest').html(beforeText);},
      start_function: function(){$('#perform-backtest').html(loaderText);},
    }

    post_request(options);

});

$(".apply-backtest-daily-price").click(function() {
    // Refreshes stock picker...


    const stock_index = $('#backtestStockPickerModalLabel').data('stock-index');
    const selected_ticker = $(this).data('ticker')
    const selected_strategy = $("#backtest-strategy-selected").data('strategy');
    $(`#selected-stock-${stock_index}`).data('ticker', selected_ticker);

    const tickers = $('[id*="selected-stock-"]').map(function() {
        return $(this).data('ticker');
    }).get();


    var options = {
      api: urls.backtest_daily_price,
      body: {
        tickers: JSON.stringify(tickers),
        strategy: selected_strategy,
      },
      complete_function: function(){
        $('.backtestStockPickerModal').modal('hide');
      },
    }

    post_request_template(options, "#backtest-stock-selection")

    updateDailyPriceChart('../..', tickers, backtestPriceChart)
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
      complete_function: function(){
        $('#backtest-parameter-form').data("number-stocks");
        $('.strategySelectModal').modal('hide');
      },
    }
    post_request_template(options, "#strategy-parameter-body");
});
