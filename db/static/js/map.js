$(document).ready(function() {
    'use strict';

    var mapboxid = $('div#map').data('mapboxid');
    var mapboxtoken = $('div#map').data('mapboxtoken');
    var lat = $('.satellite-title').data('position-lat');
    var lon = $('.satellite-title').data('position-lon');

    L.mapbox.accessToken = mapboxtoken;
    L.mapbox.config.FORCE_HTTPS = true;
    var map = L.mapbox.map('map', mapboxid, {
        zoomControl: false
    }).setView([lat, lon], 3);

    var myLayer = L.mapbox.featureLayer().addTo(map);

    var geojson = {
        type: 'FeatureCollection',
        features: [{
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "icon": {
                    "iconUrl": "/static/img/satellite-marker.png",
                    "iconSize": [32, 32],
                    "iconAnchor": [16, 16],
                }
            }
        }]
    };

    myLayer.on('layeradd', function(e) {
        var marker = e.layer,
            feature = marker.feature;

        marker.setIcon(L.icon(feature.properties.icon));
    });

    myLayer.setGeoJSON(geojson);
});
