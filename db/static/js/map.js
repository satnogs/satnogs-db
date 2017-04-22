/*global L sat_t gtk_sat_data_read_sat predict_calc Julian_Date */

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

    var sat = new sat_t();

    marker.addTo(map);

    function initialize_map(name, tle1, tle2) {
        // Load satellite orbit data from TLE
        gtk_sat_data_read_sat([name, tle1, tle2], sat);

        update_map();
    }

    function update_map() {
        // Recalculate satellite location
        var t = new Date();
        predict_calc(sat, (0, 0), Julian_Date(t));

        // Update location on map
        map.setView([sat.ssplat, sat.ssplon], 3);
        marker.setLatLng(L.latLng(sat.ssplat, sat.ssplon));
    }

    (function init_worker() {
        $.ajax({
            url: url,
            success: function(data) {
                if (('name' in data) && ('tle1' in data) && ('tle2' in data)) {
                    initialize_map(data.name, data.tle1, data.tle2);
                    setInterval(update_map, 5000);
                } else {
                    $('div#map').hide();
                }
            }
        });
    })();
});
