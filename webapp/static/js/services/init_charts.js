

var candleChartOptions = {
      series: [{data: []}],
      chart: {
          type: 'candlestick',
          height: 310,
          toolbar: true,
          zoom: {
              enabled: true,
          },
      },
      plotOptions: {
          candlestick: {
              colors: {
                  upward: '#34c38f',
                  downward: '#f46a6a'
              }
          }
      },
      xaxis: {
          type: 'datetime'
      },
      yaxis: {
          tooltip: {
              enabled: true
          }
      },
      noData: {
        text: 'Loading...'
      }
};

function createCoordinate(data) {
  return {
    x: new Date(data.date),
    y: [data.open, data.high, data.low, data.close]
  }
}

function updateDailyPriceChart(endpoint_base, ticker, chartVariable) {
  // TODO: Try to get endpoint_base to be dynamic instead of hardcoded...
  var chartOptions = {
      api: `${endpoint_base}/${urls.get_daily_price_coordinates_json}/${ticker}`,
  }
  get_chart_json(chartOptions, chartVariable)
}
