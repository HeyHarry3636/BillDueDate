// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });


$(document).ready(function() {
  // $('#rowID'+bill_id).mouseup(function() {

  $('[data-toggle="toggle"]').mouseup(function() {

    var bill_id = $(this).attr('bill_id');
    console.log("[expandTable.js] | bill_id = " + bill_id)

    $('#rowID'+bill_id).hide()



    // var bill_id = $(this).attr('bill_id');
    // console.log("[expandTable.js] | bill_id = " + bill_id)


    // $('#billDesc'+bill_id).parents().next('.hide').toggle();

    // $("#billDesc" + bill_id).click(function(){
    //   $(this).hide();
    // });
  });
});
