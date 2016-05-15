angular.module('opal.controllers').controller(
    'ObservationsController',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader
          ){

          if(!$scope.editing.observation.datetime){
              $scope.editing.observation.datetime = moment();
          }
});
