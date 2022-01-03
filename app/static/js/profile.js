$(document).ready(function(){
    $(".deleteMe").on("click", function(){
       let el_name = $(this).parents('.card-body').children('.vac-title').text();
       $(this).closest(".card").remove();
       $.ajax({
           url: '/profile',
           headers: {'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'), 'Content-Type': 'application/json'},
           method: "DELETE",
           data: JSON.stringify({"name": el_name}),
           error: function (exception) {
               console.log(exception);
               alert(exception);
           }
       })
    });
});