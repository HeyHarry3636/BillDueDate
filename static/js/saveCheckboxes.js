$(document).ready(function() {

  // $('.saveCheckboxButton').click(function () {
  //     var answer = $("#has_been_paid").val();
  //
  //     $("input:checked").each(function () {
  //         var id = $(this).attr("id");
  //
  //         alert("Do something for: " + id + ", " + answer);
  //         console.log("Do something for: " + id + ", " + answer);
  //     });
  //
  // });

  $('#has_been_paid').mouseup(function () {
      var answer = $("#has_been_paid").val();

      $(".testCheckbox").each(function () {
           var id = $(this).attr("id");

           alert("Do something for: " + id + ", " + answer);
           console.log("Do something for: " + id + ", " + answer);
       });

      // alert("Do something for: " + answer);
      // console.log("Do something for: " + answer);

  });

});
