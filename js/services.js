// satnogs-db storage

angular.module('satnogs-db')
    .factory('DBStorage', function() {
        'use strict';

        return {
            get: function() {
                return db.allDocs({include_docs: true}, function(err, response) {
                    console.log("Error: " , err);
                    console.log("Response: ", response);
                }) || [];
            },
            create: function(item, id) {
                db.put(item, id, function(err, response) {
                    console.log("Error: " + err);
                    console.log("Response: " + response);
                });
            },
            update: function(item, id, rev) {
                db.put(item, id, rev, function(err, response) {
                    console.log("Error: " + err);
                    console.log("Response: " + response);
                });
            },
            changes: function() {
                return db.changes({live: true});
            }
        };
});
