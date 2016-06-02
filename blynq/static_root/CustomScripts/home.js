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

hApp.controller('homeCtrl', ['$scope', '$window','homeDataAccessFactory', function($scope, $window, hDAF){
    var onLoad = function(){
        hDAF.getHomePageSummary(function(returnData){
            $scope.screen_count = returnData.screen_count;
            $scope.schedule_count = returnData.schedule_count
            $scope.used_storage= returnData.used_storage
            $scope.total_storage= returnData.total_storage
        })
    };
    onLoad();

    var navigationLinks = {
        screen : '/screen'
        ,content : '/content'
        ,schedule : '/schedule'
    };

    $scope.navigateTo = function(type){
        $window.location.assign(navigationLinks[type]);
    }

}]);

}());
