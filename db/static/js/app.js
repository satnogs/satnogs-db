$(document).ready(function() {
    'use strict';

    $('#search-input').focus();

    $('#search-input').keypress(function (e) {
        if (e.which == 13) {
            $('#search-form').submit();
            return false;
        }
    });

    $('#search-button').click(function (e) {
        $('#search-form').submit();
        return false;
    });
});
