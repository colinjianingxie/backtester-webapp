const settings_datatable = $('#create-setting-datatable').DataTable({
  paging: false,
});

function UID(length) {
    var result           = '';
    var characters       = '0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function deleteRow(rowId){
  settings_datatable.row("#"+rowId).remove().draw();
}

// Select2
$(".select2-search-disable").select2({
    minimumResultsForSearch: Infinity
});


$(".dataTables_length select").addClass('form-select form-select-sm');

$("#add-setting-form").on('submit', function (e) {
  const uid = UID(5);
  const form_data = e.target.elements
  const selected_ticker = form_data['select-ticker'].value
  const selected_function = form_data['select-function'].value
  const view_function_button = `<button type="button" class="btn btn-primary btn-sm btn-rounded" data-bs-toggle="modal" data-bs-target=".${selected_ticker}-${selected_function}Modal">View Details
  </button>`
  const edit_values = `<div class="d-flex gap-3">
    <a href="javascript:void(0);" class="text-success"><i class="mdi mdi-pencil font-size-18"></i></a>
    <a href="javascript:void(0);" onclick="deleteRow('${uid}')" class="text-danger"><i class="mdi mdi-delete font-size-18"></i></a>
  </div>`

  settings_datatable.row.add([selected_ticker, selected_function, view_function_button, edit_values]).node().id = uid;
  settings_datatable.draw(false);
  e.preventDefault();
});


$("#save-settings-form").on('submit', function (e) {

  e.preventDefault();
  const form_data = e.target.elements
  const settings_name = form_data['analysis-name'].value ? form_data['analysis-name'].value : `analsysis-${UID(5)}`
  const settings = settings_datatable.rows().data();
  var settings_data = []

  for (let i = 0; i < settings.length; i++) {
    var curr_row = settings[i]
    settings_data.push(`{"ticker": "${curr_row[0]}", "function": "${curr_row[1]}"}`);
  }

  if (settings_data.length === 0){
    //TODO: add error if length is 0

  }
  else{
    $.ajax({
      url:'/dashboard/create_analysis/',
      type: "POST",
      data: {"settings_data": `[${settings_data}]`, "settings_name": settings_name},
      success:function(response){
          window.location.href = `${window.location.origin}${success_url}analysis_id=${response.analysis_id}`;
      },
      complete:function(){
      },
      error:function (xhr, textStatus, thrownError){}
    });
  }



});
