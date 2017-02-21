(function(){
    'use strict';
    var mainApp =  angular.module('mainApp', ['ui.router','ui.bootstrap', 'lpApp'])
    .config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

mainApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

mainApp.config(function($locationProvider,$stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("home");

  //removes the hash for all the html5 supporting browsers. However for other, it comes
  $locationProvider.html5Mode(true).hashPrefix('!')
  //
  // Now set up the states
  $stateProvider
    .state('home', {
      url: "/home"
      ,templateUrl: "/static/templates/landingPage/home.html"
      ,controller : 'lpController'
      ,controllerAs : 'lpController'
    })
    .state('features', {
      url: "/features"
      ,templateUrl: "/static/templates/landingPage/features.html"
      // ,controller: 'screenCtrl'
      // ,controllerAs : 'screenCtrl'
    })
    .state('useCases', {
      url: "/useCases"
      ,templateUrl: "/static/templates/landingPage/useCases.html"
      // ,controller : 'groupCtrl'
      // ,controllerAs : 'groupCtrl'
    })
    .state('players',{
        url: "/players"
        ,templateUrl:'/static/templates/landingPage/players.html'
        // ,controller : 'scheduleIndexCtrl'
        // ,controllerAs : 'scheduleIndexCtrl'
    })
    .state('pricing', {
        url: "/pricing"
        ,templateUrl:'/static/templates/landingPage/pricing.html'
        // ,controller : 'layoutsIndexCtrl'
        // ,controllerAs : 'lIC'
    })
    .state('faqs', {
        url: "/faqs"
        ,templateUrl:'/static/templates/landingPage/faqs.html'
        // ,controller : 'layoutsIndexCtrl'
        // ,controllerAs : 'lIC'
    })
});

mainApp.factory("PrintToConsole", ["$rootScope", function ($rootScope) {
    var handler = { active: true };
    handler.toggle = function () { handler.active = !handler.active; };
    $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
        if (handler.active) {
            console.log("$stateChangeStart --- event, toState, toParams, fromState, fromParams");
            console.log(arguments);
        };
    });
    $rootScope.$on('$stateChangeError', function (event, toState, toParams, fromState, fromParams, error) {
        if (handler.active) {
            console.log("$stateChangeError --- event, toState, toParams, fromState, fromParams, error");
            console.log(arguments);
        };
    });
    $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
        if (handler.active) {
            console.log("$stateChangeSuccess --- event, toState, toParams, fromState, fromParams");
            console.log(arguments);
        };
    });
    $rootScope.$on('$viewContentLoading', function (event, viewConfig) {
        if (handler.active) {
            console.log("$viewContentLoading --- event, viewConfig");
            console.log(arguments);
        };
    });
    $rootScope.$on('$viewContentLoaded', function (event) {
        if (handler.active) {
            console.log("$viewContentLoaded --- event");
            console.log(arguments);
        };
    });
    $rootScope.$on('$stateNotFound', function (event, unfoundState, fromState, fromParams) {
        if (handler.active) {
            console.log("$stateNotFound --- event, unfoundState, fromState, fromParams");
            console.log(arguments);
        };
    });
    return handler;
}]);

mainApp.run(['PrintToConsole', function(PrintToConsole) {
    PrintToConsole.active = false;
}]);

})();
