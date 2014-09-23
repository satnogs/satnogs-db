$( document ).ready(function() {
    $(".plus-tip").hide();

    $( ".add-transponder" )
        .mouseover(function() {
            $( this ).find( ".plus-tip" ).show();
        })
        .mouseout(function() {
            $( this ).find( ".plus-tip" ).hide();
        });

    $( ".suggest-transponder" )
        .mouseover(function() {
            $( this ).find( ".plus-tip" ).show();
        })
        .mouseout(function() {
            $( this ).find( ".plus-tip" ).hide();
        });
});



