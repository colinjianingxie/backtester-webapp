
// Candlestick chart
// [[Timestamp], [O, H, L, C]]
function createCoordinate(data) {
  return {
    x: new Date(data.date),
    y: [data.open, data.high, data.low, data.close]
  }
}

dailyPriceData = eval(dailyPriceData)

const dailyPriceCoordinates = dailyPriceData.map(createCoordinate);

var options = {
    series: [{data: dailyPriceCoordinates}],
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
        }
};

var chart = new ApexCharts(document.querySelector("#daily-price-chart"), options);
chart.render();
