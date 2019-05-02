$(document).ready(function() {

  $('.bill-rows').mouseup(function() {
    var bill_id = $(this).attr('bill_id');
    console.log("[expandTable.js] | rowID = " + bill_id)

    $('#billDesc'+bill_id).hide()

  });
});
