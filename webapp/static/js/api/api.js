
function post_request(options){
    $.ajax({
      url:options.api,
      type: "POST",
      data: options.body,
      success:function(response){
          //successfully makes API Call, but need to verify backend.
          //successfully makes API Call, but need to verify backend.
          if (response){
            const response_status = response.status;
            const response_message = response.message;
            const response_view = response.view;
            const response_type = response.type;
            const response_data = response.data;
            if (response_status === "SUCCESS")
            {
              if (response_data == null){
                window.location.href = options.success_url;
              }
              else{
                if ('data_function' in options){
                  options.data_function(response_data);
                }
                else{
                  console.log(response_data)
                }
              }

            }
            else{
              //toastr["warning"](response_message, `${response_type} error`)
            }
          }
          else{
            //toastr["error"]("Something went wrong", "Error")
          }
      },
      complete:function(){
      },
      error:function (xhr, textStatus, thrownError){}
    });
}


function post_request_template(options, elementSelector){
    $.ajax({
      url:options.api,
      type: "POST",
      data: options.body,
      success:function(response){
          $(elementSelector).html(response);
          if ('complete_function' in options){
            options.complete_function();
          }
      },
      complete:function(){
      },
      error:function (xhr, textStatus, thrownError){}
    });
}

function get_chart_json(options, chart){
  $.ajax({
    url:options.api,
    type: "GET",
    success:function(response){
      console.log(response.data)
      chart.updateSeries([{
          data: response.data
      }])
    },
    complete:function(){
    },
    error:function (xhr, textStatus, thrownError){}
  });
}
