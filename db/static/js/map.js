/*global L */

$(document).ready(function() {
    'use strict';

    var url = $('.satellite-title').data('url');
    var mapboxid = $('div#map').data('mapboxid');
    var mapboxtoken = $('div#map').data('mapboxtoken');

    L.mapbox.accessToken = mapboxtoken;
    L.mapbox.config.FORCE_HTTPS = true;
    var map = L.mapbox.map('map', mapboxid, {
        zoomControl: false
    });

    var satIcon = L.icon({
        iconUrl: '/static/img/satellite-marker.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    var marker = L.marker([0, 0], {
        icon: satIcon,
        clickable: false
    });

    marker.addTo(map);

    function update_map(lat, lon) {
        map.setView([lat, lon], 3);

        marker.setLatLng(L.latLng(lat, lon));
    }

    (function worker() {
        $.ajax({
            url: url,
            success: function(data) {
                if (('lat' in data) && ('lon' in data)) {
                    update_map(data.lat, data.lon);
                } else {
                    $('div#map').hide();
                }
            },
            complete: function() {
                setTimeout(worker, 5000);
            }
        });
    })();
});
