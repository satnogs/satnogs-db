angular.module('satnogs-db', ['ngRoute']).config(function ($routeProvider) {
    'use strict';

    $routeProvider.when('/', {
        controller: 'SatnogsDBCtrl',
        templateUrl: 'satnogs-db-index.html'
    }).otherwise({
        redirectTo: '/'
    });

});
