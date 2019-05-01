// $(document).ready(function() {
//     $('[data-toggle="toggle"]').change(function(){
//         $(this).parents().next('.hide').toggle();
//     });
// });

$(document).ready(function() {
    $('[data-toggle="toggle"]').mouseup(function(){
        $(this).parents().next('.hide').toggle();
    });
});
