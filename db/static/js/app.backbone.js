// D3 visualisation

d3.lineChart = function(telemetry_key, unit) {
    var config = {
        margin: {top: 20, right: 20, bottom: 115, left: 100},
        width: 700,
        height: 500
    };

    var svg;

    // Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "chart-tooltip")
        .style("opacity", 0);

    function render(selection) {
        selection.each(function(_data) {
            var chartW = config.width - config.margin.left - config.margin.right,
                chartH = config.height - config.margin.top - config.margin.bottom;

            var xInterval = chartW / (_data.length - 1);

            var x1 = d3.scale.ordinal()
                .domain(_data.map(function(d, i){
                    return parseDate(d.telemetry.observation_datetime);
                }))
                .rangePoints([0, chartW]);

            var y1 = d3.scale.linear()
                .domain(d3.extent(_data, function(d, i){ return +d.telemetry.damod_data[telemetry_key]; }))
                .range([chartH, 0])
                .nice(4);

            var xAxis = d3.svg.axis()
                .scale(x1)
                .orient('bottom');

            var yAxis = d3.svg.axis()
                .scale(y1)
                .orient('left');

            if(!svg) {
                svg = d3.select(this)
                    .append('svg')
                    .classed('chart', true);
                var container = svg.append('g').classed('container-group', true);
                container.append('g').classed('chart-group', true);
                container.append('g').classed('x-axis-group axis', true);
                container.append('g').classed('y-axis-group axis', true);
            }

            svg.transition().attr({width: config.width, height: config.height});

            svg.select('.container-group')
                .attr({transform: 'translate(' + config.margin.left + ',' + config.margin.top + ')'});

            svg.select('.x-axis-group.axis')
                .attr({transform: 'translate(0,' + (chartH) + ')'})
                .transition()
                .call(xAxis);

            svg.select('.y-axis-group.axis')
                .transition()
                .call(yAxis);

            svg.selectAll(".x-axis-group.axis text")  // select all the text elements for the xaxis
                .attr("transform", function(d) {
                    return "translate(-50,50)rotate(-45)";
                });

            // Axis labels
            svg.append("text")
                    .attr("transform", "translate(" + (chartW + config.margin.right + 18) + " ," + (chartH + 10) + ")")
                    .style("text-anchor", "middle")
                    .text("Observation Datetime");

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 40)
                .attr("x", 0 - (chartH / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text("Value (" + unit + ")");

            // Define the line
            var valueline = d3.svg.line()
                .x(function(d,i) { return (xInterval*i + config.margin.left); })
                .y(function(d) { return y1(d.telemetry.damod_data[telemetry_key]) + config.margin.top; });

            // Add the valueline path
            svg.append("path")
                .attr("class", "line")
                .attr("d", valueline(_data));

            // Add the scatterplot
            svg.selectAll("dot")
                .data(_data)
                .enter().append("circle")
                .attr("r", 4)
                .attr("cx", function(d, i) { return xInterval*i + config.margin.left; })
                .attr("cy", function(d) { return y1(d.telemetry.damod_data[telemetry_key]) + config.margin.top; })
                .attr("class", "circle")
                .on("mouseover", function(d) {
                    div.transition()
                        .duration(200)
                        .style("opacity", 1);
                    div.html(d.telemetry.damod_data[telemetry_key] + ' (' + unit + ')')
                       .style("left", (d3.event.pageX) + "px")
                       .style("top", (d3.event.pageY - 26) + "px");
                    })
                .on("mouseout", function(d) {
                    div.transition()
                        .duration(500)
                        .style("opacity", 0);
                });
        });
    }
    return render;
};

// Retreive Satellite Id

var satelliteId = $('#telemetry-block').data('satid');

// Backbone Models

var TelemetryData = Backbone.Model.extend({});

// Backbone Collections

var TelemetryCollection = Backbone.Collection.extend({
    url:"/api/telemetry/?satellite=" + satelliteId
});

var TelemetryDescriptors = TelemetryCollection.extend({
    parse: function(response){
        return response[0].appendix;
    }
});

var TelemetryValues = TelemetryCollection.extend({
    comparator: function(collection){
        return( collection.get('telemetry').observation_datetime );
    },
    byDate: function (start_date, end_date) {
        filtered = this.filter(function (model) {
            var date = parseDateFilter(model.get('telemetry').observation_datetime);
            return (
                date >= start_date && date <= end_date
            )
        });
        return new TelemetryValues(filtered);
    }
});

// Backbone Views

var TelemetryDescriptorsView = Backbone.View.extend({
    el: "#telemetry-descriptors",
    template: _.template($('#telemetryDescriptorsTemplate').html()),
    initialize: function(){
        this.listenTo(this.collection, 'add reset change remove', this.renderItem);
        this.collection.fetch();
    },
    renderItem: function (model) {
        this.$el.append(this.template(model.toJSON()));
        $('#telemetry-descriptors li:first-child').addClass('active');
    }
});

var TelemetryChartView = Backbone.View.extend({
    el: ".chart",
    chart: null,
    chartSelection: null,
    initialize: function() {
        this.collection.fetch();
        _.bindAll(this, 'render', 'update');
        this.collection.on('update reset', this.render);
        chart = d3.lineChart();
    },
    events: {
        "click .telemetry-key": "update",
    },
    render: function() {
        var data = this.collection.toJSON();
        this.chartSelection = d3.select(this.el)
            .datum(data)
            .call(d3.lineChart(data[0].appendix[0].key, data[0].appendix[0].unit));
    },
    update: function(e){
        d3.select('svg').remove();
        this.chartSelection.call(d3.lineChart($(e.currentTarget).data("key"), $(e.currentTarget).data("unit")));
        var active = $(e.currentTarget);
        active.addClass('active');
        $('li').not(active).removeClass('active');
    },
});

// Fetch data and render views

var telemetryDescriptorsView = new TelemetryDescriptorsView({ collection: new TelemetryDescriptors() });
var telemetryChartView = new TelemetryChartView({collection: new TelemetryValues});


// Parse datetime values

function parseDate (date) {
    var res = date.substring(4,6) + '/' + date.substring(6,8) + '/' + date.substring(0,4) + ' ' + date.substring(9 ,11) + ':' + date.substring(11 ,13) + ':' + date.substring(13 ,15);
    return res;
}

function parseDateFilter (date) {
    var res = date.substring(0,8);
    return res;
}