app.controller('SatnogsDBCtrl', function SatnogsDBCtrl($scope, DBStorage, $routeParams) {

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
    };

    $scope.freqNum = function(value) {
        if(isNaN(value)){
          return value;
        }else{
          value = value/1000000;
          value = value.toFixed(3);
          var freq = value.toString();
          var freqFormatted = freq + " Mhz";
          return freqFormatted;
        }
     };

    $scope.$on('$viewContentLoaded', mainUI);

  });

//Modal Controllers
app.controller('ModalInstanceCtrl', function ($scope, $modalInstance, items, $routeParams) {

  $scope.ok = function () {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});

app.controller('ModalEdit', function ($scope, $modal, $log, $routeParams) {

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

//Registration Form Controller
app.controller('registrationFormCtrl', function($scope, DBStorage) {
  $scope.registrationForm = {};
  $scope.registrationForm.username = "";
  $scope.registrationForm.password = "";

  $scope.registrationForm.submit = function(item, event) {
    var username = $scope.registrationForm.username;
    var password = $scope.registrationForm.password;

    remote_db.signup(username, password, function(err, response) {
      if (err) {
        if (err.name === 'conflict') {
          $scope.error = 'Username already exists!';
        } else if (err.name === 'forbidden') {
          $scope.error = 'Invalid username/password';
        } else {
          $scope.error = 'Oops... Something bad happened';
        }
        $scope.$apply()
      }
    });
  };
});
