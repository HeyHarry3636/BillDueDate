// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });


$(document).ready(function() {
  var bill_id = $(this).attr('bill_id');
  console.log("[expandTable.js] | bill_id = " + bill_id)

  $("#billDesc" + bill_id).click(function(){
    $(this).hide();
  });
});
