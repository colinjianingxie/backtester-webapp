$(".test").click(function() {
    var ticker = $(this).data('ticker');
    var options = {
      api: urls.display_daily_price,
      body: {ticker: ticker},
      success_url: urls.display_daily_price,
    }
    post_request(options)
});
