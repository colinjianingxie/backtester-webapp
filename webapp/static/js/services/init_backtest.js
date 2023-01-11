window.onload = function() {
  const ticker = $('#stock-label-0').data('ticker');
  updateDailyPriceChart('../..', ticker, backtestPriceChart)
};

function go_to_result(response_data) {
  window.location.href = `../../${urls.backtest_result}/${response_data.backtest_id}/${response_data.backtest_result_id}`;
}

function closeBacktestStockPickerModal() {
  $('.backtestStockPickerModal').modal('hide');
}

function closeBacktestParameterModal() {
  $('.strategySelectModal').modal('hide');
}

const exampleStrategyObj = {
    'MLForecast': {
        'parameters': {
          'start_date': '2016-01-10',
          'end_date': '2017-12-31',
          'start_test_date': '2017-01-01',
        },
    },
    'MovingAverageCrossover': {
        'parameters': {
            'short_window': 100,
            'long_window': 400,
        },
    }
}

$("#initial-portfolio-value").ionRangeSlider({
  skin:"flat",
  prefix:"$",
  min:1,
  max:100000,
  from:100000,
  onChange: function (data) {
    $('#initial-backtest-value').text(`$${data.from}`);
    $('#initial-backtest-value').data('initial-capital', data.from)
  }
})



function updateStrategyParameterSelections(strategy_parameters){
  for (const [parameterName, parameterType] of Object.entries(strategy_parameters)) {
    console.log(`${parameterName}: ${parameterType}`);
  }
}
