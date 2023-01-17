window.onload = function() {
  const tickers = $('[id*="selected-stock-"]').map(function() {
      return $(this).data('ticker');
  }).get();

  updateDailyPriceChart('../..', tickers, backtestPriceChart)
};

function go_to_result(response_data) {
  window.location.href = `../../${urls.backtest_result}/${response_data.backtest_id}/${response_data.backtest_result_id}`;
}

$('#backtestStockPicker').on('show.bs.modal', function(e) {
  const idx = $(e.relatedTarget)[0].dataset.bsStockIndex;
  $('#backtestStockPickerModalLabel').text(`Stock picking ${idx}`);
  $('#backtestStockPickerModalLabel').data('stock-index', idx);
})

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
