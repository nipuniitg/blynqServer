(function(){
    'use strict';

var sPApp = angular.module("sPApp",['angularResizable']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

sPApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


//Controllers
sPApp.controller('screenPartitionIndexCtrl',[ function(){
    var sPIC = this;

    var onLoad = function(){

    }
    onLoad();


}]);

//Directives

//Factories
sPApp.factory('screenPartitionFactory',[function(){

}]);


}());
