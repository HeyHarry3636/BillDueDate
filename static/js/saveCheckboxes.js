$(document).ready(function() {

  // $('.updateButton, .bill-rows').on('click', function() {
  $('.saveCheckboxButton').is(':checked', function() {
    var checkboxStatus = $(this).val();

    req = $.ajax({
      url : '/billsPaidCheckboxes',
      type : 'POST',
      data : { bill_billpaid : checkboxStatus }
    });

    // // data = the passed back data from the app.py updateTest function
    // req.done(function(data) {
    //   $('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
    //   $('currentInput'+bank_id).val(data.bank_currentAmount);
    //   $('payDayInput'+bank_id).val(data.bank_payDayAmount);
    //   $('nextPayDateInput'+bank_id).val(data.bank_nextPayDate);
    // });

    // Do stuff for the bill rows loop through all columns


  });

});
