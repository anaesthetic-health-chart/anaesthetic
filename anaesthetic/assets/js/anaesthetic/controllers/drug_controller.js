angular.module('opal.controllers').controller(
    'DrugController',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader
          ){

          // TODO this is naughty and should be used in the wild
          // hopefuly ok for the hack day though
          var parent = $scope.$parent;
          var drugs_list = [];

          DrugLoader.then(function(drugs_list){
              drugs_list = _.reduce(drugs_list, function(memo, some_list){
                  return memo.concat(drugs_list);
              }, []);
          });
});
