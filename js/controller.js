angular.module('satnogs-db')
    .controller('SatnogsDBCtrl',
                function SatnogsDBCtrl($scope, DBStorage) {

    DBStorage.get().then(function(data) {
        docs = [];
        data.rows.forEach(function(element, index, array){
            docs.push(element.doc);
        })
        $scope.items = docs;
        console.log(docs);
        $scope.$apply();
    });

    DBStorage.changes().on('change', function() {
        DBStorage.get().then(function(data) {
            docs = [];
            data.rows.forEach(function(element, index, array){
                docs.push(element.doc);
            })
            $scope.items = docs;
            $scope.$apply();
        });
    });
});
