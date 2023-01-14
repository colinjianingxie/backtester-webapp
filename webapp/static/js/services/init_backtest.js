window.onload = function() {
  const ticker = $('#stock-label-0').data('ticker');
  updateDailyPriceChart('../..', ticker, backtestPriceChart)
};

function go_to_result(response_data) {

  window.location.href = `../../${urls.backtest_result}/${response_data.backtest_id}/${response_data.backtest_result_id}`;
  console.log(JSON.parse(response_data.backtest_returns));
  console.log(JSON.parse(response_data.backtest_indexes));
  console.log(JSON.parse(response_data.backtest_drawdowns));
  console.log(JSON.parse(response_data.backtest_portfolio_values));

  backtestResultsChart.updateOptions({
    series: [{
        name: 'backtest-returns',
        data: JSON.parse(response_data.backtest_returns)
    }],
    xaxis: {
        type: 'datetime',
        categories: JSON.parse(response_data.backtest_indexes),
    },
  });
}

function closeBacktestStockPickerModal() {
  $('.backtestStockPickerModal').modal('hide');
}

function closeBacktestParameterModal() {
  $('.strategySelectModal').modal('hide');
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
