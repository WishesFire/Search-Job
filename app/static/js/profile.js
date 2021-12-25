$(document).ready(function(){
    $(".deleteMe").on("click", function(){
       let el_name = $(this).parents('.card-body').children('.vac-title').text();
       $.ajax({
           url: '/profile',
           headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'), 'Content-Type': 'application/json'},
           method: "DELETE",
           data: JSON.stringify({"name": el_name}),
           success: function (response) {
               $(this).closest(".card").remove();
           },
           error: function (exception) {
               console.log(exception);
               alert(exception);
           }
       })
    });
});