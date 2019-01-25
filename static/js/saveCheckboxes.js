$(document).ready(function() {

  // $('.updateButton, .bill-rows').on('click', function() {
  $('.testCheckbox').mouseup(function() {
    var bill_id = $(this).attr('bill_id');
    console.log("bill_id = " + bill_id)
    var hasTheBillBeenPaid = $('#has_been_paid'+bill_id).val();
    console.log("hasTheBillBeenPaid = " + hasTheBillBeenPaid)

    // req = $.ajax({
    //   url : '/updateBankInfo',
    //   type : 'POST',
    //   data : { bank_currentAmount : currentAmount, bank_payDayAmount : payDayAmount }
    // });
    //
    // // data = the passed back data from the app.py updateTest function
    // req.done(function(data) {
    //   $('#bankSection'+bank_id).fadeOut(1000).fadeIn(1000);
    //   $('currentInput'+bank_id).val(data.bank_currentAmount);
    //   $('payDayInput'+bank_id).val(data.bank_payDayAmount);
    //   $('nextPayDateInput'+bank_id).val(data.bank_nextPayDate);
    // });
    //
    // // Do stuff for the bill rows loop through all columns


  });

});






// $(document).ready(function() {
//
//   $('#has_been_paid').mouseup(function () {
//       var answer = $("#has_been_paid").val();
//
//       $(".testCheckbox").each(function () {
//            var id = $(this).attr("id");
//
//            alert("Do something for: " + id + ", " + answer);
//            console.log("Do something for: " + id + ", " + answer);
//        });
//
//       // alert("Do something for: " + answer);
//       // console.log("Do something for: " + answer);
//
//   });
//
// });


// $(document).ready(function() {
//
//   $('.testCheckbox').each(function () {
//       // var answer = $('has_been_paid').prop("checked", true)
//       var answer = $("#has_been_paid").val();
//
//       // alert("Do something for: " + answer);
//       console.log("Do something for: " + answer);
//    });
//
// });
