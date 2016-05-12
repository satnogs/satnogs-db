// Models

var Telemetry = Backbone.Model.extend({});

/*** To deal with uri 
var TelemetryAppendix = Backbone.Model.extend({
        idAttribute: "list_id",
        urlRoot: '/api/telem',    
        initialize: function() {
            this.items = new app.ListItem;
            this.items.url = '/lists/' + this.id + '/items';
        }
    });
***/

var TelemetryCollection = Backbone.Collection.extend({
    url:"/static/telemetry.json"
});
 
var TelemetryDescriptors = TelemetryCollection.extend({
    parse: function(response){
        // Return only the nested objects that will be our models
        return response.appendix;
    }
 });

var TelemetryData = TelemetryCollection.extend({
    parse: function(response){
        // Return only the nested objects that will be our models
        return response.telemetry;
    },
    toJSON : function() {
      return this.map(function(model){ return model.toJSON(); });
    }
 });


// Views 
var TelemetryDescriptorsView = Backbone.View.extend({
    el: "#telemetry-descriptors",
    template: _.template($('#telemetryDescriptorsTemplate').html()),
    initialize: function(){
        this.listenTo(this.collection,"add", this.renderItem);          
    },
    render: function () {
        this.collection.each(function(model){
             var telemetryDescriptorsTemplate = this.template(model.toJSON());
             this.$el.append(telemetryDescriptorsTemplate);
        }, this);        
        return this;
    },
    renderItem: function(telemetryDescriptors) {
         var telemetryDescriptorsTemplate = this.template(telemetryDescriptors.toJSON());
         this.$el.append(telemetryDescriptorsTemplate);        
    }
});


var TelemetryTimeView = Backbone.View.extend({
    el: "#telemetry-viz",
    template: _.template($('#telemetryYAxisTemplate').html()),
    initialize: function(){
        this.listenTo(this.collection,"add", this.renderItem);          
    },
    render: function () {
        this.collection.each(function(model){
             var telemetryYAxisTemplate = this.template(model.toJSON());
             this.$el.append(telemetryYAxisTemplate);
        }, this);        
        return this;
    },
    renderItem: function(telemetryYAxis) {
         var telemetryYAxisTemplate = this.template(telemetryYAxis.toJSON());
         this.$el.append(telemetryYAxisTemplate);        
    }
});


////////// Bar chart


d3.custom = {};

d3.custom.barChart = function module() {
    var config = {
        margin: {top: 20, right: 20, bottom: 40, left: 40},
        width: 500,
        height: 500
    };
    var svg;

    var dispatch = d3.dispatch('customHover');

    function exports(_selection) {
        _selection.each(function(_data) {
            var chartW = config.width - config.margin.left - config.margin.right,
                chartH = config.height - config.margin.top - config.margin.bottom;

            console.log(_data.telemetry);


            var x1 = d3.scale.ordinal()
                .domain(_data.map(function(d, i){ return i; }))
                .rangeRoundBands([0, chartW], .1);

            var y1 = d3.scale.linear()
                .domain([d3.min(_data, function(d, i){ return d.damod_data.EPS_V; }), d3.max(_data, function(d, i){ return d.damod_data.EPS_V; })])
                .range([chartH, 0]);

            var xAxis = d3.svg.axis()
                .scale(x1)
                .orient('bottom');

            var yAxis = d3.svg.axis()
                .scale(y1)
                .orient('left');

            var barW = chartW / _data.length;

            if(!svg) {
                svg = d3.select(this)
                    .append('svg')
                    .classed('chart', true);
                var container = svg.append('g').classed('container-group', true);
                container.append('g').classed('chart-group', true);
                container.append('g').classed('x-axis-group axis', true);
                container.append('g').classed('y-axis-group axis', true);
            }

            svg.transition().attr({width: config.width, height: config.height})
            svg.select('.container-group')
                .attr({transform: 'translate(' + config.margin.left + ',' + config.margin.top + ')'});

            svg.select('.x-axis-group.axis')
                .attr({transform: 'translate(0,' + (chartH) + ')'})
                .transition()
                .call(xAxis);

            svg.select('.y-axis-group.axis')
                .transition()
                .call(yAxis);

            var barW = x1.rangeBand();
            var bars = svg.select('.chart-group')
                .selectAll('.bar')
                .data(_data);
            bars.enter().append('rect')
                .classed('bar', true)
                .attr({x: chartW,
                    width: barW,
                    y: function(d, i) { return 10 }, //+d.damod_data.EPS_V; },
                    height: function(d, i) { return 10 }, //chartH - +d; }
                })
                .on('mouseover', dispatch.customHover);
            bars.transition()
                .attr({
                    width: barW,
                    x: function(d, i) { return x1(i); },
                    y: function(d, i) { return y1(+d); },
                    height: function(d, i) { return chartH - y1(+d); }
                });
            bars.exit().transition().style({opacity: 0}).remove();

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


// Bar chart view
/////////////////////////////////////

var BarChartView = Backbone.View.extend({
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
    renderPlaceholder: function() {
        this.chartSelection = d3.select(this.el)
            .datum([{key: '', value: 0}])
            .call(chart);
    },
    render: function() {
        this.chartSelection = d3.select(this.el)
            .datum(this.model.get('data'))
            .call(chart);
    },
    update: function() {
        this.chartSelection.call(chart.config(this.model.get('config')));
    }
});

// Buttons view
/////////////////////////////////////

var ControlView = Backbone.View.extend({
    el: ".control",
    events: {
        "click .update-data": "updateData",
        "click .update-config": "updateConfig",
    },
    updateData: function() {
        var that = this
        var newData = d3.range(this._randomInt(10)).map(function(d, i){ return that._randomInt(100); });
        this.model.set({data: newData});
    },
    updateConfig: function() {
        var newConfig = {width: this._randomInt(600, 100)};
        this.model.set({config: newConfig});
    },
    _randomInt: function(_maxSize, _minSize){ 
        var minSize = _minSize || 1;
        return ~~(Math.random() * (_maxSize - minSize)) + minSize; 
    }
});

// Bar chart data
/////////////////////////////////////

var BarChartData = Backbone.Model.extend({
    url:"/static/telemetry.json",
    defaults: {
        data: [],
        dimension: {},
        config: {height: 200, width: 800}
    },
    parse: function(_json) {
       /* var cf = new crossfilter(_json.yt_abs_views_by_vid);
        var dimensions = this.get('dimension');
        dimensions.brands = cf.dimension(function(d) { return d.brand_name; });
        dimensions.langName = cf.dimension(function(d) { return d.lang_name; });
        var data = this._getTopOfSum('brands', 'all_time_views', 10);*/
        var data = _json.telemetry;
        this.set({data: data});
    },
  /*  filterLangBy: function(_value) {
        this.get('dimension').langName.filterExact(_value);
        this.set({data: this._getTopOfSum('brands', 'all_time_views', 10)});
    },
    _getTopOfSum: function(_dimensionName, _aggregateValueName, _topK){
        function reduceAdd(p, v){ p += v[_aggregateValueName]; return p; }
        function reduceRemove(p, v){ p -= v[_aggregateValueName]; return p; }
        function reduceInitial(){ return 0}
        var data = this.get('dimension')[_dimensionName].group()
            .reduce(reduceAdd, reduceRemove, reduceInitial)
            .top(_topK)
            .filter(function(d, i){ return d.value > 0; });
        return data;
    }*/

});


// Usage
/////////////////////////////////////

var telemetryDescriptors = new TelemetryDescriptors(); //startData);
telemetryDescriptors.fetch(); /*({
  success: function(){
    //renderCollection(); // some callback to do stuff with the collection you made
  },
  error: function(){
  }
});
*/
var telemetryDescriptorsView = new TelemetryDescriptorsView({ collection: telemetryDescriptors });
telemetryDescriptorsView.render();

var telemetryData = new TelemetryData(); //startData);
telemetryData.fetch();

var telemetryTimeView = new TelemetryTimeView({ collection: telemetryData });
telemetryTimeView.render();

var barChartModel = new BarChartData();
var controlView = new ControlView({model: barChartModel});
var barChartView = new BarChartView({model: barChartModel})

