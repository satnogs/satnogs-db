/* global Chart */

$(document).ready(function() {

    $.getJSON('/statistics/', function( data ) {

        var i;
        var r;
        var g;
        var b;
        var a;
        // Create colors for Mode Chart
        var mode_colors = [];
        for (i = 0; i < data.mode_label.length; i++) {
            r = Math.floor(data.mode_data[i]* 10);
            b = Math.floor(0.3 * 255);
            g = Math.floor(data.mode_data[i]* 10);
            a = 0.5;
            var color = 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
            mode_colors.push(color);
        }

        // Create colors for Band Chart
        var band_colors = [];
        for (i = 0; i < data.band_label.length; i++) {
            b = Math.floor(0.1 * 255);
            g = Math.floor(data.band_data[i]);
            r = Math.floor(data.band_data[i]);
            a = 0.5;
            color = 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
            band_colors.push(color);
        }

        // Global chart configuration
        Chart.defaults.global.legend.display = false;
        Chart.defaults.global.title.display = true;
        Chart.defaults.global.title.fontSize = 16;
        Chart.defaults.global.title.fontColor= '#444';

        //Mode Chart
        var mode_c = document.getElementById('modes');
        new Chart(mode_c, {
            type: 'doughnut',
            data: {
                labels: data.mode_label,
                datasets: [{
                    backgroundColor: mode_colors,
                    data: data.mode_data,
                    borderWidth: 1
                }]
            },
            options: {
                title : {
                    text: data.mode_data.length + ' Modes'
                }
            }
        });

        //Band Chart
        var band_c = document.getElementById('bands');
        new Chart(band_c, {
            type: 'doughnut',
            data: {
                labels: data.band_label,
                datasets: [{
                    backgroundColor: band_colors,
                    data: data.band_data,
                    borderWidth: 1
                }]
            },
            options: {
                title : {
                    text: data.band_data.length + ' Bands'
                }
            }
        });

        //HUD Stats
        $('#stats-alive').html(data.transmitters_alive);
        $('#stats-transmitters').html(data.transmitters);
        $('#stats-satellites').html(data.total_satellites);
    });
});
