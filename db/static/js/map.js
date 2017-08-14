/*global L Sat_t gtk_sat_data_read_sat predict_calc julian_date Geodetic_t radians xkmper de2ra asin sin cos arccos degrees pio2 pi fabs */

$(document).ready(function() {
    'use strict';

    var url = $('.satellite-title').data('url');
    var mapboxid = $('div#map').data('mapboxid');
    var mapboxtoken = $('div#map').data('mapboxtoken');

    L.mapbox.accessToken = mapboxtoken;
    L.mapbox.config.FORCE_HTTPS = true;

    // Number of positions to compute
    var COUNT = 300;

    // Interval in ms between positions to compute
    var STEP = 60*1000;

    var map = L.mapbox.map('map', mapboxid, {
        zoomControl: false
    });

    var satIcon = L.icon({
        iconUrl: '/static/img/satellite-marker.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    // Create satellite marker
    var satMarker = L.marker([0, 0], {
        icon: satIcon,
        clickable: false
    });

    // Create satellite footprint
    var satFootprint = L.polygon(
        [],
        {
            stroke: true,
            weight: 2,
            fill: true,
        }
    );

    // Create satellite orbit
    var current_orbit = [];
    var all_orbits = [];

    var satOrbit = L.multiPolyline(
        all_orbits,
        {
            weight: 4
        }
    );

    var sat = new Sat_t();

    satMarker.addTo(map);
    satFootprint.addTo(map);
    satOrbit.addTo(map);

    function initialize_map(name, tle1, tle2) {
        // Load satellite orbit data from TLE
        gtk_sat_data_read_sat([name, tle1, tle2], sat);

        {
            var t = new Date();

            var previous = 0;
            for ( var i = 0; i < COUNT; i++) {
                predict_calc(sat, (0,0), julian_date(t));
                if (Math.abs(sat.ssplon - previous) > 180) {
                    // orbit crossing -PI, PI
                    all_orbits.push(current_orbit);
                    current_orbit = [];
                }
                current_orbit.push([sat.ssplat, sat.ssplon]);
                previous = sat.ssplon;
                // Increase time for next point
                t.setTime(t.getTime() + STEP);
            }

            satOrbit.setLatLngs(all_orbits);
        }
        update_map();
    }

    function update_map() {
        // Recalculate satellite location
        var t = new Date();
        predict_calc(sat, (0, 0), julian_date(t));

        // Update location on map
        map.setView([sat.ssplat, sat.ssplon], 3);
        satMarker.setLatLng(L.latLng(sat.ssplat, sat.ssplon));

        // Refresh satellite footprint
        {
            var azi;
            // var msx, msy, ssx, ssy;
            var ssplat,
                ssplon,
                beta,
                azimuth,
                num,
                dem;
            // var rangelon, rangelat, mlon;

            var geo = new Geodetic_t();

            /* Range circle calculations.
             * Borrowed from gsat 0.9.0 by Xavier Crehueras, EB3CZS
             * who borrowed from John Magliacane, KD2BD.
             * Optimized by Alexandru Csete and William J Beksi.
             */
            ssplat = radians(sat.ssplat);
            ssplon = radians(sat.ssplon);
            beta = (0.5 * sat.footprint) / xkmper;

            var points = [];

            for (azi = 0; azi < 360; azi += 5) {
                azimuth = de2ra * azi;
                geo.lat = asin(sin(ssplat) * cos(beta) + cos(azimuth) * sin(beta)
                        * cos(ssplat));
                num = cos(beta) - (sin(ssplat) * sin(geo.lat));
                dem = cos(ssplat) * cos(geo.lat);

                if (azi == 0 && (beta > pio2 - ssplat)) {
                    geo.lon = ssplon + pi;
                }
                else if (azi == 180 && (beta > pio2 + ssplat)) {
                    geo.lon = ssplon + pi;
                }
                else if (fabs(num / dem) > 1.0) {
                    geo.lon = ssplon;
                } else {
                    if ((180 - azi) >= 0) {
                        geo.lon = ssplon - arccos(num, dem);
                    } else {
                        geo.lon = ssplon + arccos(num, dem);
                    }
                }

                points.push([degrees(geo.lat), degrees(geo.lon)]);
            }

            satFootprint.setLatLngs(points);
        }

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
