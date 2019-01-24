$('.saveCheckboxButton').click(function () {
    var answer = $("#has_been_paid").val();
    $("input:checked").each(function () {
        var id = $(this).attr("id");
        alert("Do something for: " + id + ", " + answer);
        console.log("Do something for: " + id + ", " + answer);
    });
});
