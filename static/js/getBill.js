//$(document).ready(function() {
$(function() {
	$.ajax({
		url: '/getBill',
		type: 'GET',
		success: function(response) {
			console.log(response);
		},
		error: function(error) {
			console.log(error);
		}
	});
	
	
});