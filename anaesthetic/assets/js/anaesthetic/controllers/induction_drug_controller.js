angular.module('opal.controllers').controller(
    'InductionDrugController',
    function(
        step, scope, episode, DrugLoader
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
        var drugType = _.findKey(scope.metadata.drug_type, function(drugNames){
            return _.contains(drugNames, drugName);
        })
        return {
          route: 'IV',
          drug_name: drugName,
          drug_type: drugType,
          rates: rates,
          datetime: new Date()
          //datetime: new Date(August 22 2016, 13:10:00)
        }
      });
    }
    scope.preSave = function(editing){
      editing.given_drug = _.filter(editing.given_drug, function(drug){
        return parseInt(drug.rates) != 0;

      })
    }
});
