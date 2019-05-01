// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });

$(document).ready(function() {
    $('[data-toggle="toggle"]').delegate('tr', 'click', function(){
        $(this).parents().next('.hide').toggle();
    });
});
