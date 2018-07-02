$(document).ready(function() {

  $('.updateButton').on('click', function() {
    var bank_id = $(this).attr('bank_id');

    var currentAmount = $('#currentInput'+bank_id).val();
    var payDayAmount = $('#payDayInput'+bank_id).val();

    req = $.ajax({
      url : '/testUpdate',
      type : 'POST',
      data : { bank_currentAmount : currentAmount, bank_payDayAmount : payDayAmount, bank_id : bank_id }
    });

    // data = the passed back data from the app.py updateTest function
    req.done(function(data) {
      $('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
      $('currentInput'+bank_id).val(data.bank_currentAmount);
      $('payDayInput'+bank_id).val(data.bank_payDayAmount);
    });

  });

});
