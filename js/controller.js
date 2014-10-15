angular.module('satnogs-db')
  .controller('SatnogsDBCtrl',
              function SatnogsDBCtrl($scope, DBStorage) {

    DBStorage.get().then(function(data) {
      docs = [];
      data.rows.forEach(function(element, index, array){
        docs.push(element.doc);
      });
      $scope.items = docs;
      $scope.$apply();
    });

    DBStorage.changes().on('change', function() {
      DBStorage.get().then(function(data) {
        docs = [];
        data.rows.forEach(function(element, index, array){
          docs.push(element.doc);
        });
        $scope.items = docs;
        $scope.$apply();
      });
    });

    $scope.countSatellites = function(items) {
      return Object.keys(items).length;
    };

    $scope.countTransponders = function(items) {
      var transponderCount = 0;
      for (var sat in items) {
        for (var tra in sat) {
          if(sat.hasOwnProperty(tra)){
            transponderCount++;
          }
        }
      }
      return transponderCount;
    }

    $scope.freqNum = function(value) {
        if(isNaN(value)){
          return value;
        }else{
          value = value/1000000;
          value = value.toFixed(3);
          var freq = value.toString();
          var freqFormatted = freq + " Mhz"
          return freqFormatted;
        }
     }
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
