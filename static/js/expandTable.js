// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });


$(document).ready(function() {

// FUNCTIONAL vv --------------------------------------------------
  // $('[data-toggle="toggle"]').mouseup(function() {
  //
  //   var bill_id = $(this).attr('bill_id');
  //   console.log("[expandTable.js] | bill_id = " + bill_id)
  //
  //   $('#rowID'+bill_id).hide()
// FUNCTIONAL ^^ --------------------------------------------------

$(.bill-rows).mouseup(function() {
  var bill_id = $(this).attr('bill_id');
  console.log("[expandTable.js] | rowID = " + bill_id)

  $('#rowID'+bill_id).hide()

});
