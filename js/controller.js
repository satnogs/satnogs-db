angular.module('satnogs-db')
    .controller('SatnogsDBCtrl',
                function SatnogsDBCtrl($scope, DBStorage) {

    DBStorage.get().then(function(data) {
        $scope.items = data.rows;
        $scope.$apply();
    });

    DBStorage.changes().on('change', function() {
        DBStorage.get().then(function(data) {
            $scope.items = data.rows;
            $scope.$apply();
        });
    });
});
