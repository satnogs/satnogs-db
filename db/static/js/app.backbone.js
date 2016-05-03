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
    model: Telemetry,
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

// Rendering

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



/************************************
D3 Collection
************************************/

/*var TelemetryViz = Backbone.View.extend({

  "el": "#telemetry-viz",

  initialize: function() {
    // Container el
  }

  render: function() {
    // On changes in collection, render
  }

  frame: function() {
    // on time draw
  },
 

})*/


var w = 440,
    h = 200;


var DataPoint = Backbone.Model.extend({

    initialize: function(x) {
        this.set({
            x: x
        });
    },

    type: "point",

    randomize: function() {
        this.set({
            x: Math.round(Math.random() * 10)
        });
    }

});

var DataSeries = Backbone.Collection.extend({

    model: Telemetry,

    fetch: function() {
        this.reset();
        this.add([
            new DataPoint(10),
            new DataPoint(12),
            new DataPoint(15),
            new DataPoint(18)
            ]);
    },

});

var BarGraph = Backbone.View.extend({

    "el": "#graph",

    initialize: function() {

        _.bindAll(this, "render");
        this.collection.bind("change", this.render);

        this.chart = d3.selectAll($(this.el)).append("svg").attr("class", "chart").attr("width", w).attr("height", h).append("g").attr("transform", "translate(10,15)");

        this.collection.fetch();
    },

    render: function() {

        var data = this.collection.models;

        var x = d3.scale.linear().domain([0, d3.max(data.damod_data.EPS_V, function(d) {
            return d.get("x");
        })]).range([0, w - 10]);

        var y = d3.scale.ordinal().domain([0, 1, 2, 3]).rangeBands([0, h - 20]);

        var self = this;
        var rect = this.chart.selectAll("rect").data(data.damod_data, function(d, i) {
            return i;
        });

        rect.enter().insert("rect", "text").attr("y", function(d) {
            return y(d.get("x"));
        }).attr("width", function(d) {
            return x(d.get("x"));
        }).attr("height", y.rangeBand());

        rect.transition().duration(1000).attr("width", function(d) {
            return x(d.get("x"));
        }).attr("height", y.rangeBand());

        rect.exit().remove();
        
        var text = this.chart.selectAll("text").data(data.damod_data, function(d, i) {
            return i;
        });

       text.enter().append("text")
        .attr("x", function(d) {
            return x(d.get("x"));
        })
        .attr("y", function(d,i) { return y(i) + y.rangeBand() / 2; })
        .attr("dx", -3) // padding-right
        .attr("dy", ".35em") // vertical-align: middle
        .attr("text-anchor", "end") // text-align: right
           .text(function(d) { return d.get("x");});
   
        /*this.chart.selectAll("line").data(x.ticks(10)).enter().append("line").attr("x1", x).attr("x2", x).attr("y1", 0).attr("y2", h - 10).style("stroke", "#ccc");

        this.chart.selectAll("line").data(x.ticks(10)).attr("x1", x).attr("x2", x);

        this.chart.selectAll("line").data(x.ticks(10)).exit().remove();

        this.chart.selectAll(".rule").data(x.ticks(10)).enter().append("text").attr("class", "rule").attr("x", x).attr("y", 0).attr("dy", -3).attr("text-anchor", "middle").text(String);

        this.chart.selectAll(".rule").data(x.ticks(10)).attr("x1", x).text(String);

        this.chart.selectAll(".rule").data(x.ticks(10)).exit().remove();*/
    },


});



    var dataSeries = new DataSeries();
    console.log(telemetryData);
    new BarGraph({
        collection: telemetryData
    }).render();

