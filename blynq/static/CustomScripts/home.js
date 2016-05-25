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

hApp.controller('homeCtrl', ['$scope', '$window', function($scope, $window){
    var onLoad = function(){

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
