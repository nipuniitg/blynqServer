(function(){
    'use strict';
    var mainApp =  angular.module('mainApp', ['ui.router','sdApp', 'plApp','sagApp','hApp','lApp','uDApp',
    'rApp','shApp','mwl.calendar','ui.bootstrap'])
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
      ,templateUrl: "/static/templates/home.html"
      ,controller : 'homeCtrl'
      ,controllerAs : 'homeCtrl'
    })
    .state('screens', {
      url: "/screen"
      ,templateUrl: "/static/templates/screen/screens.html"
      ,controller: 'screenCtrl'
      ,controllerAs : 'screenCtrl'
    })
    .state('groups', {
      url: "/group"
      ,templateUrl: "/static/templates/screen/groups.html"
      ,controller : 'groupCtrl'
      ,controllerAs : 'groupCtrl'
    })
    .state('playlists', {
      url: "/playlist"
      ,views : {
            '' : {
                   templateUrl: "/static/templates/playlistManagement/playlist_index.html"
                  ,controller: 'plCtrl'
                  ,controllerAs : 'plCtrl'
            },
            'content@playlists': {
                    templateUrl : '/static/templates/contentManagement/content_holder.html'
                    ,controller: 'ctCtrl'
            }
      }
    })
    .state('contentLibrary',{
        url : '/contentLibrary'
        ,views : {
            '' : { templateUrl: "/static/templates/contentManagement/content_index.html" }
            ,'content@contentLibrary' :{
                templateUrl : '/static/templates/contentManagement/content_holder.html'
                ,controller: 'ctCtrl'
            }
        }
    })
    .state('schedules',{
        url: "/schedule"
        ,templateUrl:'/static/templates/scheduleManagement/schedule_index.html'
        ,controller : 'scheduleIndexCtrl'
        ,controllerAs : 'scheduleIndexCtrl'
    })
    .state('layouts', {
        url: "/layouts"
        ,templateUrl:'/static/templates/layoutManagement/layouts_index.html'
        ,controller : 'layoutsIndexCtrl'
        ,controllerAs : 'lIC'
    })
    .state('layoutDesign',{
        url : "/layoutDesign"
        ,params: {
            layout : null
        }
        ,templateUrl : '/static/templates/layoutManagement/layout_design_index.html'
        ,controller : 'layoutDesignIndexCtrl'
        ,controllerAs : 'lDIC'
    })
    .state('reports', {
      url: "/reports"
      ,templateUrl: "/static/templates/reports/reports_index.html"
      ,controller: 'reportsIndexCtrl'
      ,controllerAs : 'reportsIndexCtrl'
    })
    .state('logout',{
        template : ' '
        ,resolve : {
            logout : ['logoutService', function(logoutService){
                logoutService();
            }]
        }
    })
    .state('changePassword', {
        url : '/changePassword'
        ,templateUrl : '/static/templates/authentication/change_password.html'
        ,controller : 'changePasswordCtrl',
        controllerAs : 'cPCtrl'
    })
    .state('updateUserDetails', {
        url : '/userDetails'
        ,templateUrl : '/static/templates/authentication/update_user_details.html'
        ,controller : 'updateUserDetailsCtrl',
        controllerAs : 'uUDCtrl'
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

mainApp.factory('logoutService',['$http','$window', function ($http, $window) {
    return function () {
        $http({
             method : "GET",
             url : '/authentication/logout'
         }).then(function mySuccess(response){
                response.data='';
                $window.location.href='';
            }, function myError(response) {
                console.log(response.statusText);
            });
    }
}]);

mainApp.config(['calendarConfig', '$uibTooltipProvider', function(calendarConfig,$uibTooltipProvider) {

    console.log(calendarConfig); //view all available config


    $uibTooltipProvider.options({
        placement : 'top'
        ,appendToBody : true
        //,trigger : ['mourseenter', 'click']
    });
    }])


}());