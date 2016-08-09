(function(){

    'use strict'
var hApp = angular.module('hApp',[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

hApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

hApp.factory('homeDataAccessFactory', ['$http', function($http){

    var getHomePageSummary = function(callback){
        $http({
            method : "GET",
            url : "/authentication/getHomePageSummaryJson"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    }
    return{
        getHomePageSummary : getHomePageSummary
    }

}]);

hApp.filter('memoryInGB',function(){
    return function(x){
        var inGB = x/1073741824;
        return inGB.toFixed(2)
    }
});

hApp.controller('homeCtrl', ['$scope','homeDataAccessFactory','$state',
 function($scope, hDAF, $state){
    var onLoad = function(){
        hDAF.getHomePageSummary(function(returnData){
            $scope.total_screen_count = returnData.total_screen_count;
            $scope.schedule_count = returnData.schedule_count;
            $scope.used_storage= returnData.used_storage;
            $scope.total_storage= returnData.total_storage;
            $scope.active_screen_count = returnData.active_screen_count;
            $scope.inactive_screen_count = returnData.inactive_screen_count;

            $scope.used_storage_percentage = ($scope.used_storage/$scope.total_storage)*100 + '%';
        })
    };
    onLoad();

    $scope.navigateTo = function(state){
        $state.go(state);
    }

}]);

}());
