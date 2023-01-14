

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

var backtestResultsOptions = {
    chart: {
        height: 350,
        type: 'area',
        toolbar: {
            show: false,
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    series: [{data: []}],
    colors: ['#556ee6'],
    xaxis: {
        type: 'datetime',
        categories: [],
    },
    grid: {
        borderColor: '#f1f1f1',
    },
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
    noData: {
      text: 'Loading...'
    }
}


function updateDailyPriceChart(endpoint_base, ticker, chartVariable) {
  // TODO: Try to get endpoint_base to be dynamic instead of hardcoded...
  var chartOptions = {
      api: `${endpoint_base}/${urls.get_daily_price_coordinates_json}/${ticker}`,
  }
  get_chart_json(chartOptions, chartVariable)
}
