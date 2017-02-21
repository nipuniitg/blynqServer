var lpApp = angular.module('lpApp',['ui.bootstrap']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

lpApp.config(function($httpProvider){
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

lpApp.factory('lpDataAccessFactory',['$http','$q',function($http, $q){

    var validateLogin = function(credentials){
        var deferred = $q.defer();
        $http({
             method : "POST"
             ,url : '/authentication/login'
             ,data : credentials
         }).then(function mySuccess(response){
                deferred.resolve(response.data);
            }, function myError(response) {
                deferred.reject(response.Text);
            });
      return deferred.promise;
    };

    var register = function(credentials){
      var deferred = $q.defer();
      $http({
        method : "POST"
        ,url : '/authentication/register'
        ,data : credentials
      }).then(function mySuccess(response){
                deferred.resolve(response.data);
            }, function myError(response) {
                deferred.reject(response.Text);
            });
      return deferred.promise;
    };

    var checkUserNameAvailability = function(username){
      var data = {
        username : username
      };
      var deferred = $q.defer();
      $http({
        method : "POST"
        ,url : '/authentication/usernameAvailability'
        ,data : data
      }).then(function mySuccess(response){
                deferred.resolve(response.data);
            }, function myError(response) {
                deferred.reject(response.Text);
            });
      return deferred.promise;
    };

    return{
        validateLogin : validateLogin
        ,register : register
        ,checkUserNameAvailability : checkUserNameAvailability
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
            lpDataAccessFactory.validateLogin(loginCtrl.credentials).then(function(data){
                if(data.success)
                {
                    $window.location.href='';
                }
                else{
                    loginCtrl.showCredentailsError = true;
                    loginCtrl.credentials = angular.copy(resetCredentials);
                }
            });
      };

      loginCtrl.cancel = function(){
        $uibModalInstance.dismiss();
      }

      onLoad();
}]);

/* signup Directive*/
lpApp.directive('signupDtv', ['$uibModal', function($uibModal){
   return{
       restrict : 'A',
       link : function(scope, elem){
           elem.bind('click', function(){
               var modalInstance = $uibModal.open({
                     animation: true
                     ,templateUrl: '/static/templates/authentication/_signup_mdl.html'
                     ,size: 'sm'
                     ,backdrop: 'static' //disables modal closing by click on the backdrop.
                     ,controller: 'signupCtrl'
                     ,controllerAs : 'signupCtrl'
               });
           })
       }
   }
}]);

lpApp.controller('signupCtrl', ['$scope','lpDataAccessFactory','$window','$uibModalInstance',
  function($scope,lpDataAccessFactory, $window, $uibModalInstance){
      var signupCtrl = this;
      var resetCredentials = {
        username : null,
        password : null,
        email : null,
        mobile_number : null,
        organization_name : null
      };

      var onLoad = function(){
        signupCtrl.showCredentailsError = false;
        signupCtrl.submitted = false;
        signupCtrl.showUsernameTakenErr = false;
        signupCtrl.checkingUsernameAvailability = false;
      }
      signupCtrl.submit = function(){
            signupCtrl.submitted = false;
            if($scope.signupForm.$invalid){
              signupCtrl.submitted = true;
              toastr.error('Please fill out the fields for signup.')
            }else{
              if(signupCtrl.showUsernameTakenErr){
                toastr.error('Please choose another username.')
              }else{
                signupCtrl.credentials.first_name = '';
                signupCtrl.credentials.last_name="";
                lpDataAccessFactory.register(signupCtrl.credentials).then(function(data){
                  if(data.success)
                  {
                    toastr.success('Thank you for signing up. We will take you to the portal in a second.');
                    lpDataAccessFactory.validateLogin(signupCtrl.credentials).then(function(data){
                        if(data.success)
                        {
                            $window.location.href='';
                        }
                        else{
                            loginCtrl.showCredentailsError = true;
                            loginCtrl.credentials = angular.copy(resetCredentials);
                        }
                    });
                  }
                  else{
                    toastr.error(data.errors.join(','));
                    signupCtrl.credentials = angular.copy(resetCredentials);
                  }
                }, function(test){
                  toastr.warning(text);
                });
              }
            }            
      }

      signupCtrl.checkUserNameAvailability = function(){
        if(signupCtrl.credentials.username.length > 0 ){
          signupCtrl.checkingUsernameAvailability = true;
          lpDataAccessFactory.checkUserNameAvailability(signupCtrl.credentials.username).then(function(data){
            signupCtrl.checkingUsernameAvailability = false;
            if(data.username_available){
              signupCtrl.showUsernameTakenErr = false;
            }else{
              signupCtrl.showUsernameTakenErr = true;
            }
          },function(){

          });
        }
        
      };

      signupCtrl.cancel = function(){
        $uibModalInstance.dismiss();
      }

      onLoad();
}]);
