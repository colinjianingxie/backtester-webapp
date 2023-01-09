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
