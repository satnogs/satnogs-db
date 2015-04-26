$(document).ready(function() {
    'use strict';

    //$('input:text').focus();

    $('input:text').keypress(function (e) {
        if (e.which == 13) {
            var term = $('input:text').val();
            $('input[name="term"]').val(term);
            $('#search-form').submit();
            return false;
        }
    });

    $('#search-button').click(function (e) {
        var term = $('input:text').val();
        $('input[name="term"]').val(term);
        $('#search-form').submit();
        return false;
    });
});
