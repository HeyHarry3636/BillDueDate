// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });

$(document).ready(function() {
    $('[data-toggle="toggle"]').delegate('label', 'click', function(){
        $(this).parents().next('.hide').toggle();
    });
});
