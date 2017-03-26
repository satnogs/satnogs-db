/* global Chart */

$(document).ready(function() {

    Chart.pluginService.register({
        afterUpdate: function (chart) {
            if (chart.config.options.elements.center) {
                var helpers = Chart.helpers;
                var centerConfig = chart.config.options.elements.center;
                var globalConfig = Chart.defaults.global;
                var ctx = chart.chart.ctx;

                var fontStyle = helpers.getValueOrDefault(centerConfig.fontStyle, globalConfig.defaultFontStyle);
                var fontFamily = helpers.getValueOrDefault(centerConfig.fontFamily, globalConfig.defaultFontFamily);

                var fontSize;

                if (centerConfig.fontSize) {
                    fontSize = centerConfig.fontSize;
                }
                // figure out the best font size, if one is not specified
                else {
                    ctx.save();
                    fontSize = helpers.getValueOrDefault(centerConfig.minFontSize, 1);
                    var maxFontSize = helpers.getValueOrDefault(centerConfig.maxFontSize, 256);
                    var maxText = helpers.getValueOrDefault(centerConfig.maxText, centerConfig.text);

                    var breakage = true;
                    do {
                        ctx.font = helpers.fontString(fontSize, fontStyle, fontFamily);
                        var textWidth = ctx.measureText(maxText).width;

                        // check if it fits, is within configured limits and that we are not simply toggling back and forth
                        if (textWidth < chart.innerRadius * 2 && fontSize < maxFontSize) {
                            fontSize += 1;
                        }
                        else {
                            // reverse last step
                            fontSize -= 1;
                            breakage = false;
                        }
                    } while (breakage);
                    ctx.restore();
                }

                // save properties
                chart.center = {
                    font: helpers.fontString(fontSize, fontStyle, fontFamily),
                    fillStyle: helpers.getValueOrDefault(centerConfig.fontColor, globalConfig.defaultFontColor)
                };
            }
        },
        afterDraw: function (chart) {
            if (chart.center) {
                var centerConfig = chart.config.options.elements.center;
                var ctx = chart.chart.ctx;

                ctx.save();
                ctx.font = chart.center.font;
                ctx.fillStyle = chart.center.fillStyle;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                var centerX = (chart.chartArea.left + chart.chartArea.right) / 2;
                var centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2;
                ctx.fillText(centerConfig.text, centerX, centerY);
                ctx.restore();
            }
        },
    });

    $.getJSON('/statistics/', function( data ) {

        var i;
        var r;
        var g;
        var b;
        var a;
        var color;
        // Create colors for Mode Chart
        var mode_colors = [];
        for (i = 0; i < data.mode_label.length; i++) {
            r = Math.floor(data.mode_data[i]* 10);
            b = Math.floor(0.3 * 255);
            g = Math.floor(data.mode_data[i]* 10);
            a = 0.5;
            color = 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
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
                elements: {
                    center: {
                        // the longest text that could appear in the center
                        maxText: '100%',
                        text: data.mode_data.length + ' Modes',
                        fontColor: '#000',
                        fontFamily: 'Helvetica Neue',
                        fontStyle: 'normal',
                        minFontSize: 1,
                        maxFontSize: 20,
                    }
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
                elements: {
                    center: {
                        // the longest text that could appear in the center
                        maxText: '100%',
                        text: data.band_data.length + ' Bands',
                        fontColor: '#000',
                        fontFamily: 'Helvetica Neue',
                        fontStyle: 'normal',
                        minFontSize: 1,
                        maxFontSize: 20,
                    }
                }
            }
        });

        //HUD Stats
        $('#stats-alive').html(data.transmitters_alive);
        $('#stats-transmitters').html(data.transmitters);
        $('#stats-satellites').html(data.total_satellites);
        $('#stats-data').html(data.total_data);
    });
});
