// satnogs-db storage

app.factory('DBStorage', function() {
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

app.factory('Auth', function($rootScope) {
    var currentUser = {
        loggedIn: false,
        username: ''
    };

    return {
      isLoggedIn: function() {
          return currentUser.loggedIn;
      },

      getUserName: function() {
          return currentUser.username;
      },

      logOut: function () {
          currentUser.loggedIn = false;
          currentUser.username = '';
          $rootScope.$broadcast('userChanged', currentUser);
      },

      logIn: function (username) {
          currentUser.loggedIn = true;
          currentUser.username = username;
          $rootScope.$broadcast('userChanged', currentUser);
      }

    };
});
