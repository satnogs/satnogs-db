var app = angular.module('satnogs-db', ['ngRoute', 'ui.bootstrap']);

app.config(function ($routeProvider){
    'use strict';

    $routeProvider
      .when('/', {
        templateUrl: 'templates/main.html',
        controller: 'SatnogsDBCtrl'
      })
      .when('/login', {
        templateUrl: 'templates/login.html'
      })
      .when('/signup', {
        templateUrl: 'templates/signup.html'
      })
      .otherwise({
        redirectTo: '/'
      });

});
