// Retreive Satellite Id

var satelliteId = $('#telemetry-block').data('satid');

// Models

var Telemetry = Backbone.Model.extend({});

var TelemetryData = Backbone.Model.extend({
    url:"/api/telemetry/?satellite=" + satelliteId,
    defaults: {
        data: [],
        dimension: {},
        config: {height: 500, width: 700}
    },
    parse: function(_json) {
        var data = _json;
        this.set({data: data});
    },
});

// Collections

var TelemetryCollection = Backbone.Collection.extend({
    url:"/api/telemetry/?satellite=" + satelliteId
});

var TelemetryDescriptors = TelemetryCollection.extend({
    parse: function(response){
        return response[0].appendix;
    }
 });


// Views

var TelemetryDescriptorsView = Backbone.View.extend({
    el: "#telemetry-descriptors",
    template: _.template($('#telemetryDescriptorsTemplate').html()),
    initialize: function(){
        this.listenTo(this.collection, 'add reset change remove', this.renderItem);
        this.collection.fetch();
    },
    render: function () {
        this.collection.each(function(model){
            this.$el.append(this.template(model.toJSON()));
        }, this);
        return this;
    },
    renderItem: function (model) {
        this.$el.append(this.template(model.toJSON()));
    }
});

// D3 Visualisation

d3.custom = {};

d3.custom.barChart = function module(telemetry_key) {
    var config = {
        margin: {top: 20, right: 20, bottom: 60, left: 60},
        width: 700,
        height: 500
    };
    var svg;

    var dispatch = d3.dispatch('customHover');

    function exports(_selection) {
        _selection.each(function(_data) {
            var chartW = config.width - config.margin.left - config.margin.right,
                chartH = config.height - config.margin.top - config.margin.bottom;

            var x1 = d3.scale.ordinal()
                .domain(_data.map(function(d, i){
                    return parseDate(d.telemetry.observation_datetime);
                }))
                .rangeRoundBands([0, chartW], 0.1);

            var y1 = d3.scale.linear()
                .domain([0, d3.max(_data, function(d, i){ return +d.telemetry.damod_data[telemetry_key]; })])
                .range([chartH, 0])
                .nice(4);

            var xAxis = d3.svg.axis()
                .scale(x1)
                .orient('bottom');

            var yAxis = d3.svg.axis()
                .scale(y1)
                .orient('left');

            var xInterval = chartW / _data.length;

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


            // Axis labels
            svg.append("text")
                    .attr("transform", "translate(" + (chartW + config.margin.right + 18) + " ," + (chartH + 10) + ")")
                    .style("text-anchor", "middle")
                    .text("Observation Datetime");

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0)
                .attr("x", 0 - (chartH / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text("Value");

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
                .attr("r", 3.5)
                .attr("cx", function(d, i) { return xInterval*i + config.margin.left; })
                .attr("cy", function(d) { return y1(d.telemetry.damod_data[telemetry_key]) + config.margin.top; });

        });
    }
    exports.config = function(_newConfig) {
        if (!arguments.length) return width;
        for(var x in _newConfig) if(x in config) config[x] = _newConfig[x];
        return this;
    };
    d3.rebind(exports, dispatch, 'on');
    return exports;
};


function parseDate (date) {
    var res = date.substring(9 ,11) + ':' + date.substring(11 ,13) + ':' + date.substring(13 ,15) + ' ' + date.substring(4,6) + '/' + date.substring(6,8) + '/' + date.substring(0,4);
    return res;
}

var TelemetryVizView = Backbone.View.extend({
    el: ".chart",
    chart: null,
    chartSelection: null,
    initialize: function() {
        var that = this;
        this.model.fetch();
        _.bindAll(this, 'render', 'update');
        this.model.bind('change:data', this.render);
        this.model.bind('change:config', this.update);
        chart = d3.custom.barChart();
        chart.config(this.model.get('config'));
        chart.on('customHover', function(d, i){ console.log('hover', d, i); });
        this.renderPlaceholder();
    },
    events: {
        "click .telemetry-key": "update",
    },
    renderPlaceholder: function() {
        this.chartSelection = d3.select(this.el)
            .datum([{key: '', value: 0}])
            .call(d3.custom.barChart(this.model.get('data')[0].appendix[1].key));
    },
    render: function() {
        this.chartSelection = d3.select(this.el)
            .datum(this.model.get('data'))
            .call(d3.custom.barChart(this.model.get('data')[0].appendix[1].key));
    },
    update: function(e){
        d3.select("svg").remove();
        this.chartSelection.call(d3.custom.barChart($(e.currentTarget).attr('id')));
    },
});



// Fetch data and render views

var telemetryDescriptorsView = new TelemetryDescriptorsView({ collection: new TelemetryDescriptors() });
var telemetryDataModel = new TelemetryData();
var telemetryVizView = new TelemetryVizView({model: telemetryDataModel});
