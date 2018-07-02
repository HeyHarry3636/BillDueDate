$(document).ready(function() {

  $('.updateButton').on('click', function() {
    var bank_id = $(this).attr('bank_id');

    var currentAmount = $('#currentInput'+bank_id).val();
    var payDayAmount = $('#payDayInput'+bank_id).val();

    req = $.ajaz({
      url : '/testUpdate',
      type : 'POST',
      data : { bank_currentAmount : currentAmount, bank_payDayAmount : payDayAmount, bank_id : bank_id }
    });

    req.done(function(data) {
      $('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
    });

  });

});
