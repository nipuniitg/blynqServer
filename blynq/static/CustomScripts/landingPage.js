var lpApp = angular.module('lpApp',['ui.bootstrap']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

lpApp.config(function($httpProvider){
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

lpApp.factory('lpDataAccessFactory',['$http',function($http){

    var validateLogin = function(credentials, callback){
        $http({
             method : "POST"
             ,url : '/authentication/login'
             ,data : credentials
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                toastr.error('Oops! Some error. Please refresh the page and login again.')
                console.log(response.statusText);
            });
    }

    return{
        validateLogin : validateLogin
    }

}]);

lpApp.controller('lpController', ['$http','$scope','$timeout', function($http, $scope, $timeout){
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
             ,url : '/api/requestQuote'
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

    $scope.selectPlan = function(planType){
        resetForm();
        $scope.requestQuoteFormDetails.additional_details = 'Hi, we would like to opt for '+planType+' plan. Your additional comments goes here.....'
    }

    $scope.becomepartner = function(partnerType){
        resetForm();
        var yourcomments = "Write your comments here."
        switch (partnerType) {
            case "advertiser" : 
                $scope.requestQuoteFormDetails.additional_details = 'Hi, I would like to advertise on your network';
                break;
            case "contentpartner":
                $scope.requestQuoteFormDetails.additional_details = 'Hi, I would like to become a content partner.';
                break;
            case "screenpartner" : 
                $scope.requestQuoteFormDetails.additional_details = 'Hi, I have a great footfall around my screens. And I would like to generate revenue through it. ';
                break;
        }
    }
    onLoad();
}]);


/* login Directive*/
lpApp.directive('loginDtv', ['$uibModal', function($uibModal){
   return{
       restrict : 'A',
       link : function(scope, elem){
           elem.bind('click', function(){
               var modalInstance = $uibModal.open({
                     animation: true
                     ,templateUrl: '/static/templates/authentication/_login_mdl.html'
                     ,size: 'sm'
                     ,backdrop: 'static' //disables modal closing by click on the backdrop.
                     ,controller: 'loginCtrl'
                     ,controllerAs : 'loginCtrl'
               });
           })
       }
   }

}]);

lpApp.controller('loginCtrl', ['$scope','lpDataAccessFactory','$window','$uibModalInstance',
  function($scope,lpDataAccessFactory, $window, $uibModalInstance){
      var loginCtrl = this;
      var resetCredentials = {
        username : null,
        password : null
      }

      var onLoad = function(){
        loginCtrl.showCredentailsError = false;
      }
      loginCtrl.submit = function(){
            lpDataAccessFactory.validateLogin(loginCtrl.credentials, function(data){
                if(!data.success)
                {
                    loginCtrl.showCredentailsError = true;
                    loginCtrl.credentials = angular.copy(resetCredentials);
                }
                else{
                    $window.location.href='';
                }

            });
      }

      loginCtrl.cancel = function(){
        $uibModalInstance.dismiss();
      }

      onLoad();
}]);
