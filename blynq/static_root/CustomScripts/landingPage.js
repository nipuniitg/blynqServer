var lpApp = angular.module('lpApp',['ui.bootstrap']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

lpApp.config(function($httpProvider){
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

lpApp.controller('formController', ['$http','$scope','$timeout', function($http, $scope, $timeout){
    var defaultFormDetails = {
        name : ''
        ,email : ''
        ,mobile_number : null
        ,num_of_devices : null
        ,additional_details : ''
    };

    var onLoad = function(){
        $scope.showSuccessAlert = false;
        $scope.showErrorAlert = false;
    };

    var resetForm = function(){
        $scope.requestQuoteFormDetails = angular.copy(defaultFormDetails);
        $scope.requestQuoteForm.$setPristine();
        $scope.requestQuoteForm.$setUntouched();
    };


    $scope.submit = function(){
        $http({
             method : "POST"
             ,url : '/requestQuote'
             ,data : $scope.requestQuoteFormDetails
         }).then(function mySucces(response){
                $scope.showSuccessAlert = true;
                $timeout(function(){
                    $scope.showSuccessAlert = false
                }, 10000);
                resetForm();
            }, function myError(response) {
                $scope.showErrorAlert = true;
                $timeout(function(){
                    $scope.showErrorAlert = false
                }, 5000);
                console.log(response.statusText);
            });
    };

    onLoad();
}]);