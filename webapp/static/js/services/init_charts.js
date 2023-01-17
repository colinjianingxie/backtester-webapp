

var candleChartOptions = {
      series: [],
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

var backtestReturnsOptions = {
    chart: {
      height: 380,
      type: 'line',
      zoom: {
        enabled: false
      },
      toolbar: {
        show: false
      }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    series: [],
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

var backtestDrawdownsOptions = {
    chart: {
      height: 380,
      type: 'line',
      zoom: {
        enabled: false
      },
      toolbar: {
        show: false
      }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    series: [],
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

var backtestValuesOptions = {
    chart: {
      height: 380,
      type: 'line',
      zoom: {
        enabled: false
      },
      toolbar: {
        show: false
      }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 3,
    },
    series: [],
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

function updateDailyPriceChart(endpoint_base, tickers, chartVariable) {
  // TODO: Try to get endpoint_base to be dynamic instead of hardcoded...
  for(const ticker of tickers){
    var chartOptions = {
        api: `${endpoint_base}/${urls.get_daily_price_coordinates_json}/${ticker}`,
    }
    get_chart_json(chartOptions, chartVariable)
  }
}

var backtestReturnsChart = new ApexCharts(document.querySelector("#backtest-returns-chart"), backtestReturnsOptions);
var backtestDrawdownsChart = new ApexCharts(document.querySelector("#backtest-drawdowns-chart"), backtestDrawdownsOptions);
var backtestValuesChart = new ApexCharts(document.querySelector("#backtest-values-chart"), backtestValuesOptions);
var backtestPriceChart = new ApexCharts(document.querySelector("#backtest-daily-price-chart"), candleChartOptions);
