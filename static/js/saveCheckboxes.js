var sList = "";
$('.saveCheckboxButton').on('click', function() {
  $('input:checked').each(function () {
      var sThisVal = ($(this).checked ? "1" : "0");
      sList += (sList=="" ? sThisVal : "," + sThisVal);
  });
});
console.log (sList);
