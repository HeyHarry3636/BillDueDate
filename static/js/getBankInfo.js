$(document).ready(function() {

  // $('.updateButton, .bill-rows').on('click', function() {
  $('.updateButton').on('click', function() {
    var bank_id = $(this).attr('bank_id');

    var currentAmount = $('#currentInput'+bank_id).val();
    var payDayAmount = $('#payDayInput'+bank_id).val();
    var nextPayDayDate = $('#nextPayDateInput'+bank_id).val();
    var projectedMonths = $('#projectedMonths'+bank_id).val();

    req = $.ajax({
      url : '/updateBankInfo',
      type : 'POST',
      data : {
        bank_currentAmount : currentAmount,
        bank_payDayAmount : payDayAmount,
        bank_nextPayDate : nextPayDayDate,
        bank_id : bank_id,
        bank_projectedMonths : projectedMonths
      },
      success: function(response) {
        refreshedPage = $(response);
        newData = refreshedPage.find('#billTable').html();
        $('#billTable').html(newData);
        // $('#billTable').html(response);
      }
    });

    // data = the passed back data from the app.py updateTest function
    req.done(function(data) {
      //$('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
      $('currentInput'+bank_id).val(data.bank_currentAmount);
      $('payDayInput'+bank_id).val(data.bank_payDayAmount);
      $('nextPayDateInput'+bank_id).val(data.bank_nextPayDate);
      $('projectedMonths'+bank_id).val(data.bank_projectedMonths);
      // location.reload();
    });

    // Do stuff for the bill rows loop through all columns


  });

});
