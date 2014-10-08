$(document).ready(function () {
    $(document).on("mouseover", ".add-transponder", function(){
        $(this).find(".plus-tip").show();
    });
    $(document).on("mouseout", ".add-transponder", function(){
        $(this).find(".plus-tip").hide();
    });

    $(document).on("mouseover", ".suggest-transponder", function(){
        $(this).find(".plus-tip").show();
    });
    $(document).on("mouseout", ".suggest-transponder", function(){
        $(this).find(".plus-tip").hide();
    });

    $(".satellite-search").keypress( function(){
        $(".satellite-panels").show();
        $(".info").hide();
        $(".stats").hide();
    });
});
