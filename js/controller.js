angular.module('satnogs-db')
    .controller('SatnogsDBCtrl',
                function SatnogsDBCtrl($scope, $routeParams, $filter, DBstorage) {

    var items = $scope.todos = DBStorage.get();
    
});
