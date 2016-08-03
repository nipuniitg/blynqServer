(function(){
    'use strict';

    //User Details App
    var uDApp =  angular.module('uDApp',[])
    .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

    uDApp.config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

    uDApp.factory('uDDataAccessFactory',['$http','$q', function($http,$q){
        var changePassword = function(passwordsObj){
            var deferred = $q.defer();
            $http({
                 method : "POST"
                 ,url : '/authentication/changePassword'
                 ,data : passwordsObj
             }).then(function mySuccess(response){
                    deferred.resolve(response.data);
                }, function myError(response) {
                    deferred.reject();
                });

                return deferred.promise
            }

        var updateUserDetails = function(userDetails){
            var deferred = $q.defer();
            $http({
                 method : "POST"
                 ,url : '/authentication/updateUserDetails'
                 ,data : userDetails
             }).then(function mySuccess(response){
                    deferred.resolve(response.data);
                }, function myError(response) {
                    deferred.reject();
                });

                return deferred.promise
        }

        var getUserDetails = function(){
            var deferred = $q.defer();
            $http({
                 method : "GET"
                 ,url : '/authentication/getUserDetails'
             }).then(function mySuccess(response){
                    deferred.resolve(response.data);
                }, function myError(response) {
                    deferred.reject();
                });

            return deferred.promise
        }

        return{
            changePassword : changePassword
            ,updateUserDetails : updateUserDetails
            ,getUserDetails : getUserDetails
        }
    }])

    uDApp.controller('changePasswordCtrl',['$scope','uDDataAccessFactory','$timeout','$state',
     function($scope,uDAF,$timeout,$state){
        var cPCtrl = this;
        var onLoad = function(){
            cPCtrl.passwordsMatch = true;
        }

        onLoad();

        cPCtrl.changePassword = function(){
            if($scope.changePasswordForm.$valid && cPCtrl.passwordsMatch){
                var passwordsObj = {
                    current_password :  cPCtrl.current_password,
                    new_password : cPCtrl.new_password,
                    reenter_new_password : cPCtrl.reenter_new_password
                }
                uDAF.changePassword(passwordsObj).then(function(data){
                    if(data.success){
                        toastr.success('Password updated successfully. Please login again.');
                        $timeout(function(){
                            $state.go('logout');
                        }, 5*1000);
                    }
                    else{
                        toastr.warning(data.errors.join(','));
                    }
                },function(response){
                    toastr.error('Oops! Some error occured. Please refresh the page and try again.');
                    console.log(response.statusText);
                });
            }else{
                toastr.warning('Some errors found in the form. Please correct them and try again.')
            }
        }

        $scope.$watchGroup([ function(){
            return cPCtrl.new_password
        }, function(){
            return  cPCtrl.reenter_new_password
        }], function (newVals) {
            if(newVals[0] !== 'undefined' && newVals[1] !== 'undefined'){
                if(newVals[0] !== newVals[1]){
                    cPCtrl.passwordsMatch = false;
                }else{
                    cPCtrl.passwordsMatch = true;
                }
            }
        });

    }]);

    uDApp.controller('updateUserDetailsCtrl',['$scope','uDDataAccessFactory',function($scope,uDAF){
        var uUDCtrl = this;
        uUDCtrl.userDetails={};

        var onLoad = function(){
            uUDCtrl.refreshDetails();
        };

        uUDCtrl.refreshDetails = function(){
            uDAF.getUserDetails().then(function(data){
                uUDCtrl.userDetails = data;
            },function(){
                toastr.warning('Oops!There was some error while loading user details. Please refresh the page and try again.')
            });
        }

        onLoad();

        uUDCtrl.updateUserDetails = function(){
            if($scope.userDetailsForm.$valid){
                uDAF.updateUserDetails(uUDCtrl.userDetails).then(function(data){
                    if(data.success){
                        uUDCtrl.refreshDetails();
                        toastr.success('Details saved successfully');
                    }else{
                        toastr.warning(data.errors.join(','));
                    }
                },function(response){
                    toastr.error('Oops! Some error occured. Please refresh the page and try again.');
                    console.log(response.statusText);
                });
            }else{
                toastr.warning('There are some errors in the form. Please correct them and try again.')
            }

        }

    }]);

}());