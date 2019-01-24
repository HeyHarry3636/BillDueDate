var sList = "";
$('input[type=checkbox]').each(function () {
    var sThisVal = (this.checked ? "1" : "0");
    sList += (sList=="" ? sThisVal : "," + sThisVal);
});
console.log (sList);
