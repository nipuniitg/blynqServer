
var myModule = angular.module("myApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

myModule.controller("myCntrl", function($scope, $http){
$http({
        method : "GET",
        url : "getscreens"
    }).then(function mySucces(response) {
        $scope.screens = response.data;
        /*$log.log(response.data);*/
    }, function myError(response) {
        $scope.message = response.statusText;
    });

});

