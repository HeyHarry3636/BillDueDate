$(function() {
    $("td[colspan=3]").find("p").hide();
    $("table").click(function(event) {
        event.stopPropagation();
        var $target = $(event.target);
        if ( $target.closest("td").attr("colspan") > 1 ) {
            $target.slideUp();
            $target.closest("tr").prev().find("td:first").html("+");
        } else {
            $target.closest("tr").next().find("p").slideToggle();
            if ($target.closest("tr").find("td:first").html() == "+")
                $target.closest("tr").find("td:first").html("-");
            else
                $target.closest("tr").find("td:first").html("+");
        }
    });
});
