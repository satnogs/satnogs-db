angular.module('satnogs-db')
    .controller('SatnogsDBCtrl',
                function SatnogsDBCtrl($scope, DBStorage) {

    DBStorage.get().then(function(data) {
        docs = [];
        data.rows.forEach(function(element, index, array){
            docs.push(element.doc);
        })
        $scope.items = docs;
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

//Modal Controllers
angular.module('satnogs-db').controller('ModalInstanceCtrl', function ($scope, $modalInstance, items) {

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

angular.module('satnogs-db').controller('ModalEdit', function ($scope, $modal, $log) {

  $scope.open = function (size) {
    var modalInstance = $modal.open({
      templateUrl: 'modal_edit.html',
      controller: 'ModalInstanceCtrl',
      size: size,
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

  };
});