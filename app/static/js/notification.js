$(document).ready(function(){
	$('.content_toggle').click(function(){
		$('.content_block').slideToggle(300);
		$('.content_toggle').remove();
		let vacancy_slug = $('.slug-vacancy').text();
		$.ajax({
           url: "/vacancy/" + vacancy_slug,
           headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'), 'Content-Type': 'application/json'},
           method: "POST",
           data: JSON.stringify({"notification": true}),
           error: function (exception) {
               console.log(exception);
               alert("Something wrong");
           }
       })
	});
});