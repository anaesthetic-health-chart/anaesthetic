angular.module('opal.records').factory('ObservationRecord', function(){
  return function(record){
      if(!record.id){
          if(!record.datetime){
              record.datetime = moment()
          }
      }
      return record;
    }
});
