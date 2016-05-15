angular.module('opal.controllers').controller(
    'DrugController',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite, $q,
            $cookieStore, DrugLoader
          ){

          // TODO this is naughty and should be used in the wild
          // hopefuly ok for the hack day though
          var self = this;
          this.drugs_list = [];
          this.drug_types = [];

          DrugLoader.then(function(drugs_list){
              self.drugs_list = _.reduce(drugs_list, function(memo, some_list){
                  return memo.concat(some_list);
              }, []);

              self.drug_types = _.keys(drugs_list);

              var setDrug = function(nv){
                  _.each(drugs_list, function(v, k){
                      if(v.indexOf(nv) != -1){
                          $scope.editing.given_drug.drug_type = k;
                      }
                  });
              };
              $scope.$watch('editing.given_drug.drug_name', setDrug);
          });




});
