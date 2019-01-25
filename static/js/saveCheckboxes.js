$(document).ready(function() {

  // $('.updateButton, .bill-rows').on('click', function() {
  $('.testCheckbox').mouseup(function() {
    var bill_id = $(this).attr('bill_id');
    console.log("[saveCheckboxes.js] | bill_id = " + bill_id)

    var hasTheBillBeenPaid = !$('#has_been_paid'+bill_id).is(':checked');
    console.log("[saveCheckboxes.js] | hasTheBillBeenPaid = " + hasTheBillBeenPaid)

    req = $.ajax({
      url : '/billsPaidCheckboxes',
      type : 'POST',
      data : { bill_billId : bill_id, bill_billPaid : hasTheBillBeenPaid }
    });

    // data = the passed back data from the app.py updateTest function
    req.done(function(data) {
      $('#has_been_paid'+bill_id).fadeOut(1000).fadeIn(1000);
      // $('currentInput'+bank_id).val(data.bank_currentAmount);
    });

  });

});
