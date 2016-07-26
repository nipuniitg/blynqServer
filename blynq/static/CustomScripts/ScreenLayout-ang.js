(function(){
    'use strict';

var sPApp = angular.module("sPApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

sPApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


/* screen Layouts index*/
//Controllers
sPApp.controller('screenLayoutsIndexCtrl',['$scope', 'screenLayoutsIndexFactory','blueprints', '$state','$uibModal',
 function($scope, sLIF,blueprints, $state, $uibModal){
    var sLIC = this;

    var onLoad = function(){
        sLIF.getScreenLayouts().then(function getScreenLayoutsSuccess(layouts){
            sLIC.screenLayouts = layouts;
        },function getScreenLayoutsReject(){
            toastr.warning('Oops! some error occurred while fetching screen layouts. Please refresh page and try again')
        });
    }

    sLIC.createNewLayout = function(){
        $state.go('layoutDesign');
    }
    onLoad();
}]);

//Factories
sPApp.factory('screenLayoutsIndexFactory',['$http','$q', function($http, $q){
    var getScreenLayouts = function(){
        var deferred = $q.defer();
        $http({
            method : "GET",
            url : "/api/screenLayouts/getScreenLayouts"
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    return{
        getScreenLayouts : getScreenLayouts
    }

}]);
/* end- screen Layouts index */


/* screen Layouts Design index */

sPApp.factory('layoutDesignFactory',['$http', '$q',
 function($http, $q){

    var upsertScreenLayout = function(screenLayout){
        var deferred = $q.defer();

        $http({
            method : "GET",
            url : "/api/screenLayouts/upsertScreenLayout",
            data : screenLayout
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    return{
        upsertScreenLayout : upsertScreenLayout
    }

 }]);

sPApp.controller('layoutDesignIndexCtrl', ['$scope','$stateParams','blueprints','constantsAndDefaults',
'layoutDesignFactory',
 function($scope, sP, blueprints, cAD, lDF){
    /*
        Below controller is the key controller
        which connects to Pane properties,
        toolbar, editor-pane directives.
        This controls the active pane.
    */
    var lDIC = this;
    var parentCanvas = angular.element(document.getElementsByClassName('canvas'));

    var onLoad = function(){
        // selecting default screenType (portrait/landscape/resolution)
        $scope.screenTypes = cAD.getScreenTypes();


        //layout obtained from stateParams
        $scope.screenLayout = sP.screenLayout;
        if($scope.screenLayout == null){
            var newLayout = new blueprints.ScreenLayout();
            newLayout.panes.push(new blueprints.LayoutPane(0));
            $scope.screenLayout = newLayout;
            $scope.screenLayout.screen_type = $scope.screenTypes[0];
        }

        setCanvasDimensions();

        lDIC.selected_screen_type = angular.copy($scope.screenLayout.screen_type);
        lDIC.resetScreenLayoutBackup = angular.copy($scope.screenLayout);
        $scope.activePaneIndex = 0;
    };

    var setCanvasDimensions = function(){
        parentCanvas.css({
            height : parentCanvas.width()*($scope.screenLayout.screen_type.height/$scope.screenLayout.screen_type.width)
        });
    }

    lDIC.screenTypeChanged = function(){
        //set layout
        var newLayout = new blueprints.ScreenLayout();
        newLayout.panes.push(new blueprints.LayoutPane(0));
        $scope.screenLayout = newLayout;
        $scope.screenLayout.screen_type = angular.copy(lDIC.selected_screen_type);

        //set new layout defaults
        lDIC.resetScreenLayoutBackup = angular.copy($scope.screenLayout);
        $scope.activePaneIndex = 0;

        //set canvas heights accroding to the resolution selected
        setCanvasDimensions();
    }

    lDIC.addPane = function(){
        $scope.screenLayout.panes.push(new blueprints.LayoutPane($scope.screenLayout.panes.length));
        $scope.activePaneIndex = $scope.screenLayout.panes.length-1;
        toastr.success('Pane added')
    }

    lDIC.deletePane = function(){
        $scope.screenLayout.panes.splice($scope.activePaneIndex, 1);
        if($scope.activePaneIndex != 0){
            $scope.activePaneIndex = 0;
        }
        else{
            $scope.activePaneIndex = 1;
        }
        toastr.success('Pane deleted.')
    }

    lDIC.saveLayout = function(){
        lDF.upsertScreenLayout($scope.screenLayout).then(function resolved(data){
            if(data.success){
                toastr.success('layout saved');
            }
        }, function upsertFail(){
                toastr.warning('Oops! There was some error. Please try again.')
        })
    };

    lDIC.resetLayout = function(){
        $scope.screenLayout = angular.copy(lDIC.resetScreenLayoutBackup);
        toastr.success('layout reset complete');
    }

    /*Todo : Below method is currently used from directive(paneTemplate).
      And in all incontroller locations, the index update is done directly.
       Look for a better solution.*/
    $scope.updateActivePane = function(index){
        $scope.$apply(function(){
            $scope.activePaneIndex = angular.copy(index);
        });
        //paneToDirectiveSrv.setActivePaneIndex();
    }


    onLoad();

}]);

sPApp.directive('paneTemplate',['constantsAndDefaults',
  function(cAD){
    /*
        This directive has isolate scope and is
        responsible for resizable, draggable and onclick function
        which makes a pane active and others inactive.
     */
return{
    restrict : 'AE',
    scope : {
        activePaneIndex : '='
        ,updateActivePaneIndex : '&updateActivePaneFn'
        ,paneObj : '=pane'
        ,index : '='
    }
    ,templateUrl : '/static/templates/screenLayout/_editor_pane_template.html'
    ,link: function($scope, element, attr) {
        //declarations
        var parentCanvas = angular.element(document.getElementsByClassName('canvas'));
        var draggableConfig = {
            disabled : true
            ,revert : false
            ,containment : '.canvas'
            ,appendTo:'body'
            ,drag : function(event, ui){
                            var margin_left_in_percentage = getPercentage(ui.position.left, parentCanvas.width());
                            var margin_top_in_percentage = getPercentage(ui.position.top, parentCanvas.height());
                            $scope.$apply(function(){
                                $scope.paneObj.margin_left = margin_left_in_percentage;
                                $scope.paneObj.margin_top = margin_top_in_percentage;
                            });
                        }

        };
        var resizableConfig = {
            disabled : true
            ,containment : '.canvas'
            ,handles : 'all'
            ,minWidth: cAD.getPaneDefaults().minWidth
            ,minHeight : cAD.getPaneDefaults().minHeight
            ,resize : function(event, ui){
                        var width_in_percentage = getPercentage(ui.size.width, parentCanvas.width());
                        var height_in_percentage = getPercentage(ui.size.height, parentCanvas.height());
                        $scope.$apply(function(){
                            if(ui.size.width > cAD.getPaneDefaults().minWidth && ui.size.height > cAD.getPaneDefaults().minHeight){
                                $scope.paneObj.height = height_in_percentage
                                $scope.paneObj.width = width_in_percentage
                            }
                            else{
                                toastr.warning('You cannot minimize further')
                            }
                        });
                    }
        };

        var getPercentage = function(nume, deno){
            return Math.round(((nume/deno) * 100))
        }

        var paneDiv = element[0].getElementsByClassName('pane');
        paneDiv = angular.element(paneDiv);

        paneDiv.draggable(draggableConfig);

        paneDiv.resizable(resizableConfig);

        paneDiv.bind('click',function(){
            $scope.updateActivePaneIndex()($scope.index);
        });

        var enableActivePaneProperties = function(){
            paneDiv.draggable( "option", "disabled", false );
            paneDiv.resizable( "option", "disabled", false );
        }

        var disableActivePaneProperties = function(){
            paneDiv.draggable( "option", "disabled", true );
            paneDiv.resizable( "option", "disabled", true );
        }

        $scope.$watch('activePaneIndex', function(newVal, oldVal){
            if( $scope.index == newVal ){
                enableActivePaneProperties();
                $scope.setActiveClass = true;
            }
            else{
                if($scope.index == oldVal ){
                    disableActivePaneProperties();
                }
                $scope.setActiveClass = false;
            }
        }, true);



    }
}

}])

sPApp.directive('paneProperties', [function(){
    /*
        This directive has scope of its
        parent which is layoutDesignIndexCtrl.
     */
    return{
        restrict : 'E'
        ,templateUrl : '/static/templates/screenLayout/_pane_properties.html'
        ,link : function ($scope, elem, attr){
        }
    }

}]);

sPApp.directive('layoutProperties', [function(){
    /*
        This directive has scope of its
        parent which is layoutDesignIndexCtrl.
     */
    return{
        restrict : 'E'
        ,templateUrl : '/static/templates/screenLayout/_layout_properties.html'
        ,link : function ($scope, elem, attr){
        }
    }

}]);

/* end screen Layouts Design index */
}());
