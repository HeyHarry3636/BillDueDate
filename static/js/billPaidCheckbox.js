$(document).ready(function() {

  $('.checkedBox').on('click', function() {

    // req = $.ajax({
    //   url : '/updateBillPaidInfo',
    //   type : 'POST',
    //   data : { bank_currentAmount : currentAmount, bank_payDayAmount : payDayAmount, bank_nextPayDate : nextPayDayDate, bank_id : bank_id }
    // });

    req = $.ajax({
      url : '/updateBillPaidInfo',
      type : 'POST',
      data : {}
    });
    // data = the passed back data from the app.py updateTest function
    // req.done(function(data) {
    //   $('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
    //   $('currentInput'+bank_id).val(data.bank_currentAmount);
    //   $('payDayInput'+bank_id).val(data.bank_payDayAmount);
    //   $('nextPayDateInput'+bank_id).val(data.bank_nextPayDate);
    // });

    // Do stuff for the bill rows loop through all columns


  });

});
