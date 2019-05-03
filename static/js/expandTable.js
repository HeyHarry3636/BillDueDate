$(document).ready(function() {

// FUNCTIONAL vv --------------------------------------------------
  // $('.bill-rows').mouseup(function() {
  //   var bill_id = $(this).attr('bill_id');
  //   console.log("[expandTable.js] | rowID = " + bill_id)
  //
  //   $('#billDesc'+bill_id).hide()
  // });
// FUNCTIONAL ^^ --------------------------------------------------

// FUNCTIONAL vv --------------------------------------------------
  // $('.bill-rows').mouseup(function() {
  //   var bill_id = $(this).attr('bill_id');
  //   console.log("[expandTable.js] | bill_id = " + bill_id)
  //
  //   $('#billDesc'+bill_id).toggle()
  // });
// FUNCTIONAL ^^ --------------------------------------------------

  $('.bill-rows').mouseup(function() {
    var bill_id = $(this).attr('bill_id');
    //console.log("[expandTable.js] | bill_id = " + bill_id)

    $('#billDesc'+bill_id).toggle();

  });
});
