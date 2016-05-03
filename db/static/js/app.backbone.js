// Models

var Telemetry = Backbone.Model.extend({
    urlRoot:"//db.satnogs.org/",
});
 
var TelemetryCollection = Backbone.Collection.extend({
    model: Telemetry,
    url:"/static/telemetry.json"
});
 
// Views 
var TelemetryView = Backbone.View.extend({
    el: "#telemetry",
    template: _.template($('#telemetryTemplate').html()),
    initialize: function(){
        this.listenTo(this.collection,"add", this.renderItem);          
    },
    render: function () {
        this.collection.each(function(model){
             var telemetryTemplate = this.template(model.toJSON());
             this.$el.append(telemetryTemplate);
        }, this);        
        return this;
    },
    renderItem: function(telemetry) {
         var telemetryTemplate = this.template(telemetry.toJSON());
         this.$el.append(telemetryTemplate);        
    }
});


var telemetryCollection = new TelemetryCollection(); //startData);

telemetryCollection.fetch(); /*({
  success: function(){
    //renderCollection(); // some callback to do stuff with the collection you made
  },
  error: function(){
  }
});
*/

var telemetryView = new TelemetryView({ collection: telemetryCollection });
telemetryView.render();
