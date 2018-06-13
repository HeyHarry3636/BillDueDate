$(function() {
    $('#btnAddBill').click(function() {
 
        $.ajax({
            url: '/addBill',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});