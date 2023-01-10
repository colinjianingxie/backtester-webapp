function createCoordinate(data) {
  return {
    x: new Date(data.date),
    y: [data.open, data.high, data.low, data.close]
  }
}

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
