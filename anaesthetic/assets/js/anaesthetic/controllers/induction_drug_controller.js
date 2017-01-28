angular.module('opal.controllers').controller(
    'InductionDrugController',
    function(
        step, scope, episode
      ){
    "use strict";

    var DRUGS = {
      "propofol": 200,
      "atracurium": 0,
      "fentanyl": 100
    };

    if(!_.isArray(scope.editing.given_drug)){
      scope.editing.given_drug = [scope.editing.given_drug];
    }

    scope.editing.given_drug = _.filter(scope.editing.given_drug, function(givenDrug){
      return _.contains(_.keys(DRUGS), givenDrug.drug_name);
    });


    if(!scope.editing.given_drug.length){
      scope.editing.given_drug = _.map(DRUGS, function(rates, drugName){
        return {
          drug_name: drugName,
          rates: rates
        }
      });
    }
});
