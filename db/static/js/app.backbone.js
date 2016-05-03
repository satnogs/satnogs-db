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

