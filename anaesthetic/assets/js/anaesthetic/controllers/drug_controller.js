angular.module('opal.controllers').controller('DrugController', function($scope, slugifyFilter){
  var setDrug = function(nv){
    _.each($scope.metadata.drug_type, function(v, k){
      if(_.contains(v, nv)){
        $scope.editing.given_drug.drug_type = k;
      }
    });
  };

  if(!$scope.editing.given_drug.id){
    $scope.editing.given_drug.datetime = new Date();
  }
  $scope.$watch('editing.given_drug.drug_name', setDrug);
});
