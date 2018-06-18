$(document).ready(function() {
	$.ajax({
		url: '/getBill',
		type: 'GET',
		success: function(response) {
			window.location="/userHome";
			console.log(response);
		},
		error: function(error) {
			console.log(error);
		}
	});
});