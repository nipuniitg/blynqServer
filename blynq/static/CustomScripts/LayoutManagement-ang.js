(function(){
    'use strict';
//layout App
var lApp = angular.module("lApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

lApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


/* screen Layouts index*/
//Controllers
lApp.controller('layoutsIndexCtrl',['$scope', 'layoutsIndexFactory','blueprints', '$state','$uibModal',
 function($scope, lIF,blueprints, $state, $uibModal){
    var lIC = this;

    var onLoad = function(){
        refreshLayouts();
    }

    var refreshLayouts = function(){
        lIF.getCustomLayouts().then(function getLayoutsSuccess(layouts){
            lIC.layouts = layouts;
        },function getLayoutsReject(){
            toastr.warning('Oops! some error occurred while fetching screen layouts. Please refresh page and try again')
        });
    }

    lIC.createNewLayout = function(){
        $state.go('layoutDesign');
    }

    lIC.editLayout = function(index){
        $state.go('layoutDesign', {layout : lIC.layouts[index]});
    }

    lIC.deleteLayout = function(index){
        var delete_layout_id = lIC.layouts[index].layout_id;
        lIF.deleteLayout(delete_layout_id).then(function deleteSuccess(data){
            if(data.success){
                toastr.success('layout deleted');
                refreshLayouts();
            }
            else{
                toastr.warning(data.errors.join(','));
                console.log(data.errors);
            }
        }, function(data){
            toastr.warning('Oops! Some error occurred.');
        })
    }
    onLoad();
}]);

//Factories
lApp.factory('layoutsIndexFactory',['$http','$q', function($http, $q){

    var getCustomLayouts = function(){
        var deferred = $q.defer();
        $http({
            method : "GET",
            url : "/api/layout/getLayouts"
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    var deleteLayout = function(delete_layout_id){
        var deferred = $q.defer();
        var postData = {
            layout_id : delete_layout_id
        }

        $http({
            method : "POST",
            url : "/api/layout/deleteLayout",
            data : postData
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    return{
        getCustomLayouts : getCustomLayouts
        ,deleteLayout : deleteLayout
    }

}]);
/* end- screen Layouts index */


/* screen Layouts Design index */

lApp.factory('layoutDesignFactory',['$http', '$q',
 function($http, $q){

    var upsertLayout = function(layout){
        var deferred = $q.defer();

        $http({
            method : "POST",
            url : "/api/layout/upsertLayout",
            data : layout
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    var getAspectRatios = function(){
        var deferred = $q.defer();
        $http({
            method : "GET",
            url : "/api/screen/getAspectRatios"
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    return{
        upsertLayout : upsertLayout
        ,getAspectRatios : getAspectRatios
    }

 }]);

lApp.controller('layoutDesignIndexCtrl', ['$scope','$stateParams','blueprints','constantsAndDefaults',
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
        // selecting default aspectRatio (portrait/landscape/resolution)
        lDF.getAspectRatios().then(function getAspectRatiosSuccess(data){
            $scope.aspectRatios = data;
            //layout obtained from stateParams
            $scope.layout = sP.layout;
            if($scope.layout == null){
                var newLayout = new blueprints.Layout();
                newLayout.layout_panes.push(new blueprints.LayoutPane(0));
                $scope.layout = newLayout;
                $scope.layout.aspect_ratio = $scope.aspectRatios[0];
            }

            setCanvasDimensions();

            lDIC.selected_aspect_ratio = angular.copy($scope.layout.aspect_ratio);
            lDIC.resetLayoutBackup = angular.copy($scope.layout);
            $scope.activePaneIndex = 0;

            //setActiveTabIndex
            setActiveTabIndex(0);
        },function reject(){

        })



    };

    var setCanvasDimensions = function(){
        var computed_height;
        if($scope.layout.aspect_ratio.orientation == 'LANDSCAPE'){
            //width*(orientationHeightComponent/orientationWidthComponent)
            computed_height = parentCanvas.width()*($scope.layout.aspect_ratio.height_component/$scope.layout.aspect_ratio.width_component)
        }
        else{
            computed_height =  parentCanvas.width()*($scope.layout.aspect_ratio.width_component/$scope.layout.aspect_ratio.height_component)
        }

        parentCanvas.css({
            height : computed_height
        });
    }

    var setActiveTabIndex = function(index){
        $scope.activeTabIndex = index;
    }

    lDIC.aspectRatioChanged = function(){
        //set layout
        var newLayout = new blueprints.Layout();
        newLayout.layout_panes.push(new blueprints.LayoutPane(0));
        $scope.layout = newLayout;
        $scope.layout.aspect_ratio = angular.copy(lDIC.selected_aspect_ratio);

        //set new layout defaults
        lDIC.resetLayoutBackup = angular.copy($scope.layout);
        $scope.activePaneIndex = 0;

        //set canvas heights accroding to the resolution selected
        setCanvasDimensions();
    }

    lDIC.addPane = function(){
        $scope.layout.layout_panes.push(new blueprints.LayoutPane($scope.layout.layout_panes.length));
        $scope.activePaneIndex = $scope.layout.layout_panes.length-1;
        toastr.success('Pane added')

        setActiveTabIndex(1);
    }

    lDIC.deletePane = function(){
        $scope.layout.layout_panes.splice($scope.activePaneIndex, 1);
        if($scope.activePaneIndex != 0){
            $scope.activePaneIndex = 0;
        }
        else{
            $scope.activePaneIndex = 1;
        }
        toastr.success('Pane deleted.')
    }

    lDIC.saveLayout = function(){
        lDF.upsertLayout($scope.layout).then(function resolved(data){
            if(data.success){
                $scope.layout.layout_id = angular.copy(data.saved_layout.layout_id);
                toastr.success('layout saved');
            }
        }, function upsertFail(){
                toastr.warning('Oops! There was some error. Please try again.')
        })
    };

    lDIC.resetLayout = function(){
        $scope.layout = angular.copy(lDIC.resetLayoutBackup);
        toastr.success('layout reset complete');
    }

    /*Todo : Below method is currently used from directive(paneTemplate).
      And in all incontroller locations, the index update is done directly.
       Look for a better solution.*/
    $scope.updateActivePane = function(index){
        $scope.$apply(function(){
            $scope.activePaneIndex = angular.copy(index);
            setActiveTabIndex(1);
        });
        //paneToDirectiveSrv.setActivePaneIndex();
    }

    onLoad();

}]);

lApp.directive('paneTemplate',['constantsAndDefaults',
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
    ,templateUrl : '/static/templates/layoutManagement/_editor_pane_template.html'
    ,link: function($scope, element, attr) {
        //declarations
        var parentCanvas = angular.element(document.getElementsByClassName('canvas'));
        var draggableConfig = {
            disabled : true
            ,revert : false
            ,containment : '.canvas'
            ,appendTo:'body'
            ,drag : function(event, ui){
                            var left_margin_in_percentage = getPercentage(ui.position.left, parentCanvas.width());
                            var top_margin_in_percentage = getPercentage(ui.position.top, parentCanvas.height());
                            $scope.$apply(function(){
                                $scope.paneObj.left_margin = left_margin_in_percentage;
                                $scope.paneObj.top_margin = top_margin_in_percentage;
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

lApp.directive('paneProperties', [function(){
    /*
        This directive has scope of its
        parent which is layoutDesignIndexCtrl.
     */
    return{
        restrict : 'E'
        ,templateUrl : '/static/templates/layoutManagement/_pane_properties.html'
        ,link : function ($scope, elem, attr){
        }
    }

}]);

lApp.directive('layoutProperties', [function(){
    /*
        This directive has scope of its
        parent which is layoutDesignIndexCtrl.
     */
    return{
        restrict : 'E'
        ,templateUrl : '/static/templates/layoutManagement/_layout_properties.html'
        ,link : function ($scope, elem, attr){
        }
    }

}]);

/* end screen Layouts Design index */
}());
