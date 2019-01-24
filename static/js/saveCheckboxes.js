var sList = "";
$('.saveCheckboxButton').on('click', function() {
  $('input:checked').each(function () {
    var sThisVal = ($(this).checked ? "1" : "0");
    sList += (sList=="" ? sThisVal : "," + sThisVal);
  });
});
console.log(sList);
alert(sList);

// $('.saveCheckboxButton').click(function () {
//     var answer = $("#has_been_paid").val();
//     $("input:checked").each(function () {
//         var id = $(this).attr("id");
//         alert("Do something for: " + id + ", " + answer);
//     });
// });
