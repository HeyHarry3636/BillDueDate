$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
/*             success: function(response) {
                console.log(response);
            }, */
			      success: function(response) {
                window.location.href=console.log(response.redirect);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
