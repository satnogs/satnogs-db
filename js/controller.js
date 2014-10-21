app.controller('MainCtrl', function MainCtrl($scope, Auth) {

    $scope.loggedIn = Auth.isLoggedIn();
    $scope.username = Auth.getUserName;

    $scope.logout = function() {
        remote_db.logout(function(err, respone) {
            if (!err) {
                Auth.logOut();
            }
        });
    };

    $scope.$on('userChanged', function(event, x) {
        $scope.loggedIn = x.loggedIn;
        $scope.username = x.username;
        $scope.$apply();
    });
});

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
app.controller('registrationFormCtrl', function($scope, $location, DBStorage, Auth) {

  if (Auth.isLoggedIn()) {
    $location.path('/');
  }

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
      } else {
        $location.path('/');
      }
      $scope.$apply();
    });
  };
});

//Login Form Controller
app.controller('loginFormCtrl', function($scope, $rootScope, $location, DBStorage, Auth) {
  $scope.loginForm = {};
  $scope.loginForm.username = "";
  $scope.loginForm.password = "";

  if (Auth.isLoggedIn()) {
    $location.path('/');
  }

  $scope.loginForm.submit = function(item, event) {
    var username = $scope.loginForm.username;
    var password = $scope.loginForm.password;

    remote_db.login(username, password, function(err, response) {
      if (err) {
        if (err.name === 'unauthorized') {
          $scope.error = 'Name or password incorrect!';
        } else {
          $scope.error = 'Oops... Something bad happened';
        }
      } else {
        Auth.logIn(response.name);
        $location.path('/');
      }
      $scope.$apply();
    });
  };
});
