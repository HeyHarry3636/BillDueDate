// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });


$(document).ready(function() {

// FUNCTIONAL vv --------------------------------------------------
  // $('.bill-rows').mouseup(function() {
  //   var bill_id = $(this).attr('bill_id');
  //   console.log("[expandTable.js] | rowID = " + bill_id)
  //
  //   $('#billDesc'+bill_id).hide()
  // });
// FUNCTIONAL ^^ --------------------------------------------------

  $('.bill-rows').mouseup(function() {
    var bill_id = $(this).attr('bill_id');
    console.log("[expandTable.js] | rowID = " + bill_id)

    $('#billDesc'+bill_id).toggle()
  });

});
