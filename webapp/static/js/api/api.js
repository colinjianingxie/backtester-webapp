function post_request(options){
    $.ajax({
      url:options.api,
      type: "POST",
      data: options.body,
      success:function(response){
          //successfully makes API Call, but need to verify backend.
          console.log("HERE: ", response)
      },
      complete:function(){
      },
      error:function (xhr, textStatus, thrownError){}
    });
}
