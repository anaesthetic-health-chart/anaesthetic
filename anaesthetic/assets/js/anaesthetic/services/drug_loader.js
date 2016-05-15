angular.module('opal.services').factory('DrugLoader', function($q, $http, $window) {
    var deferred = $q.defer();
    var url = '/anaesthetic/drugs_list/';
    $http({ cache: true, url: url, method: 'GET'}).then(function(response) {
      deferred.resolve(response.data);
    }, function() {
	    // handle error better
	    $window.alert('Drugs could not be loaded');
    });

    return deferred.promise;
});
