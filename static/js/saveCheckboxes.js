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
      $('#has_been_paid'+bill_id).fadeOut(200).fadeIn(200);
      // $('.bill-rows').fadeOut(200).fadeIn(200);

      var billTable = document.getElementByClassName("bill-rows");
      billTable.refresh();

      // Need the DataTable extension, included on the layout.html page
      // $('.bill-rows').DataTable().ajax.reload();
      // $('.testClass').DataTable().ajax.reload();


      // $('.bill-rows').load('/dashboard');
      // $('.bill-rows').html(data);
      // location.reload();

      // $('.bill-rows').DataTable().ajax.reload();

      // $('.bill-rows').each(function() {
      //   console.log("testEach")

    });

  });

});
