$(document).ready(function() {
    'use strict';

    $('.satellite-group-item').each(function() {
        var img = $(this).data('image');
        $(this).find('.panel-heading').css('background-image', 'url(' + img + ')');
    });
});
