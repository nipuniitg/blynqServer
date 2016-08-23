var rApp = angular.module("rApp",['chart.js']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

rApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

//Reports index page
rApp.factory('reportsIndexFactory', ['$http','$q','cookDateTime',
function($http, $q, cDT){

    //private methods
    var cookedFilterset = function(filterset){

        if('start_time' in filterset){
            filterset.start_time = cDT.getOnlyTime(filterset.start_time)
        }

        if('end_time' in filterset){
            filterset.end_time = cDT.getOnlyTime(filterset.end_time)
        }

        if('start_date' in filterset){
            filterset.start_date = cDT.getOnlyDate(filterset.start_date)
        }

        if('end_date' in filterset){
            filterset.end_date = cDT.getOnlyDate(filterset.end_date)
        }

        return filterset
    }

    //public methods
    var getScreensReportData = function(filterset){
        var postData = {
            filterset : cookedFilterset(angular.copy(filterset))
        }
        var deferred = $q.defer();
        $http({
            method : "GET"
            ,url : "/api/reports/screen"
            ,params : postData
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    var getPlaylistsReportData = function(filterset){
        var postData = {
            filterset : filterset
        }
        var deferred = $q.defer();
        $http({
            method : "GET"
            ,url : "/api/reports/playlist"
            ,params : postData
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    var geContentReportData = function(filterset){
        var postData = {
            filterset : filterset
        }
        var deferred = $q.defer();
        $http({
            method : "GET"
            ,url : "/api/reports/media"
            ,params : postData
        }).then(function mySucces(response) {
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    }

    return{
        getScreensReportData : getScreensReportData
        ,getPlaylistsReportData : getPlaylistsReportData
        ,geContentReportData : geContentReportData
    }

}]);

rApp.controller('reportsIndexCtrl',['$scope', function($scope){
    var reportsIndexCtrl =  this;

}]);

//Screens tab
rApp.directive('screensReportsTab',[ function(){
    /*
        Directive Type : samescope
        Description : This directive provides reports pertained to screens. Such as, online duration.
    */
    var controllerFunction = ['$scope','reportsIndexFactory',
        function($scope, rIF){

        var scrRprtsCtrl = this;

        var onLoad = function(){

            //$scope.refreshScreensData();
        }

        $scope.refreshScreensData = function(filterset){
            /*
                filterset object is only passed when the user selects any filters.
                Otherwise the filterset is not passed.
            */
            rIF.getScreensReportData(filterset).then(function(screensData){
                //This is the data which should be distributed to charts and tables.
                $scope.data = screensData;
            },function(text){
                toastr.warning('Oops! some error occured while fetching data.Please refresh the page and try again.')
            });
        }

        //select filter fields
        scrRprtsCtrl.optionalFiltersChoices = {
            screens : true
            ,playlists : false
            ,content_files : false
        }

        //line - chart data
        $scope.labels = ["January", "February", "March", "April", "May", "June", "July", "January", "February", "March", "April", "May", "June", "July","January", "February", "March", "April", "May", "June", "July"];
        $scope.series = ['Series A', 'Series B'];
        $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
        ];
        $scope.onClick = function (points, evt) {
        console.log(points, evt);
        };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
        title: {
            display: true,
            text: 'Screens Active Hours'
        },
        scales: {
          yAxes: [
            {
              id: 'y-axis-1',
              type: 'linear',
              display: true,
              position: 'left'
            },
            {
              id: 'y-axis-2',
              type: 'linear',
              display: true,
              position: 'right'
            }
          ]
        }
        };

        //pie chart - data
        $scope.pieLabels = ["online", "offline"];
        $scope.pieData = [300, 100];


        }]

    return{
        restrict : 'E'
        ,scope : true
        ,templateUrl : '/static/templates/reports/_screen_reports_tab.html'
        ,controller : controllerFunction
        ,controllerAs : 'scrRprtsCtrl'
    }

}]);

//Playlists tab
rApp.directive('playlistsReportsTab',[function(){
    /*
        Directive Type : samescope
        Description : This directive provides reports pertained to playlists.
        How much time each playlist ran in the give period of time.
    */
    var controllerFunction = ['$scope','reportsIndexFactory',
        function($scope, rIF){

        var pylRprtsCtrl = this;

        var onLoad = function(){
            //$scope.refreshPlaylistsData();
        }

        $scope.refreshPlaylistsData = function(filterset){
            /*
                filterset object is only passed when the user selects any filters.
                Otherwise the filterset is not passed.
            */
            rIF.getPlaylistsReportData(filterset).then(function(playlistsData){
                //This is the data which should be distributed to charts and tables.
                $scope.data = playlistsData;
            },function(text){
                toastr.warning('Oops! some error occured while fetching data.Please refresh the page and try again.')
            });
        }

        //select filter fields
        pylRprtsCtrl.optionalFiltersChoices = {
            screens : true
            ,playlists : true
            ,content_files : false
        }

        //line - chart data
        $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
        $scope.series = ['Series A', 'Series B'];
        $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
        ];
        $scope.onClick = function (points, evt) {
        console.log(points, evt);
        };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
        scales: {
          yAxes: [
            {
              id: 'y-axis-1',
              type: 'linear',
              display: true,
              position: 'left'
            },
            {
              id: 'y-axis-2',
              type: 'linear',
              display: true,
              position: 'right'
            }
          ]
        }
        };

        //pie chart - data
        $scope.pieLabels = ["online", "offline"];
        $scope.pieData = [300, 100];


        }]

    return{
        restrict : 'E'
        ,scope : true
        ,templateUrl : '/static/templates/reports/_playlists_reports_tab.html'
        ,controller : controllerFunction
        ,controllerAs : 'pylRprtsCtrl'
    }
}]);

//Content tab
rApp.directive('contentReportsTab',[function(){
    /*
        Directive Type : samescope
        Description : This directive provides reports pertained to content files. Such as, online duration.
    */
    var controllerFunction = ['$scope','reportsIndexFactory',
        function($scope, rIF){

        var cntRprtsCtrl = this;

        var onLoad = function(){
            //$scope.refreshContentData();
        }

        $scope.refreshContentData = function(filterset){
            /*
                filterset object is only passed when the user selects any filters.
                Otherwise the filterset is not passed.
            */
            rIF.geContentReportData(filterset).then(function(contentData){
                //This is the data which should be distributed to charts and tables.
                $scope.data = contentData;
            },function(text){
                toastr.warning('Oops! some error occured while fetching data.Please refresh the page and try again.')
            });
        }

        //select filter fields
        cntRprtsCtrl.optionalFiltersChoices = {
            screens : true
            ,playlists : true
            ,content_files : true
        }

        //line - chart data
        $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
        $scope.series = ['Series A', 'Series B'];
        $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
        ];
        $scope.onClick = function (points, evt) {
        console.log(points, evt);
        };
        $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }];
        $scope.options = {
        scales: {
          yAxes: [
            {
              id: 'y-axis-1',
              type: 'linear',
              display: true,
              position: 'left'
            },
            {
              id: 'y-axis-2',
              type: 'linear',
              display: true,
              position: 'right'
            }
          ]
        }
        };

        //pie chart - data
        $scope.pieLabels = ["online", "offline"];
        $scope.pieData = [300, 100];


        }]

    return{
        restrict : 'E'
        ,scope : true
        ,templateUrl : '/static/templates/reports/_content_reports_tab.html'
        ,controller : controllerFunction
        ,controllerAs : 'cntRprtsCtrl'
    }
}]);


//Filter Set
rApp.factory('filtersFactory',['blueprints','dataAccessFactory','$q','plDataAccessFactory','constantsAndDefaults',
 function(bp, sDAF,$q, pDF, cAD ){
    //Private
    /* List containing all screens with  */
    var selectedBoolSetter = function(allItems, selectedItems, key, isAllSelected){
        /*
            returns all items with a boolean 'selected', true incase it is selected by user.
            'isAllSelected' tells if every item is selected.
            'selectedItems' doesnt possess any objects first time and hence this bool.
        */

        var r = []
        ,allItemsLength = allItems.length;
        if (typeof(selectedItems) !== 'undefined'){
            selectedItemsLength = selectedItems.length;
        }
        for(i=0; i<allItemsLength; i++){
            var item = allItems[i];
            if(isAllSelected){
                item['selected'] = !0;
            }else{
                if(typeof(selectedItemsLength) !== 'undefined')
                {
                    for(l=0; l<selectedItemsLength; l++){
                        if(item[key] == selectedItems[l][key]){
                            //set selected bool
                            item['selected']= !0;
                            selectedItemsLength -= 1;
                            selectedItems.splice(l,1);
                            break;
                        }
                        }
                }
                if(!item['selected']){
                    item['selected'] = !1;
                }
            }
            r.push(item);
        }
        return r;

    }

    //Public
    var getFilterSet = function(options){
        //constructor function from base class BaseFilterSet
        //Need to be restructured, as every properties are going into prototype.
        var FilterSet = function FilterSet(){};
        FilterSet.prototype = new bp.BaseFilterSet();

        if(options.screens){
            FilterSet.prototype.screens = [];
            FilterSet.prototype.all_screens=true;
        }

        if(options.playlists){
            FilterSet.prototype.playlists=[];
            FilterSet.prototype.all_playlists = true;
        }

        if(options.content_files){
            FilterSet.prototype.content_files = [];
            FilterSet.prototype.all_content_files = true;
        }

        var filterset = new FilterSet();

        return filterset
    };

    var getAllScreenListWithSelectedBool = function(selectedScreens, isAllSelected){
        var deferred = $q.defer();
        sDAF.getAllScreens(function(allScreens){
            var allScreensWithSelectedBool = selectedBoolSetter(allScreens, selectedScreens, 'screen_id', isAllSelected);
            deferred.resolve(allScreensWithSelectedBool)
        })

        return deferred.promise
    }

    var getAllPlaylistsListWithSelectedBool = function(selectedPlaylists, isAllSelected){
        var deferred = $q.defer();
        pDF.getPlaylists(function(allPlaylists){
            var allPlaylistsWithSelectedBool = selectedBoolSetter(allPlaylists, selectedPlaylists, 'playlist_id', isAllSelected);
            deferred.resolve(allPlaylistsWithSelectedBool)
        })

        return deferred.promise
    }

    var getAllContentListWithSelectedBool = function(selectedContent, isAllSelected){
        var deferred = $q.defer();
        pDF.getFolderContentsRecursively(cAD.getAllFilesHomeFolder(), function(allContent){
            var allContentWithSelectedBool = selectedBoolSetter(allContent, selectedContent, 'content_id', isAllSelected);
            deferred.resolve(allContentWithSelectedBool)
        })

        return deferred.promise
    }

    var getSelectedItems = function(allItems){
        /*
            returnObj has two properties.
            1. selected Items - only selected items
            2. isAllSelected - a boolean which tells if all items are selected.(which is used in filter-textbox)
        */
        var returnObj = {};
        var selectedItems = [];
        var isAllSelected = !0;
        var allItemsLength = allItems.length;
        for(i=0; i<allItemsLength; i++){
            if(allItems[i].selected){
                delete allItems[i].selected;
                selectedItems.push(allItems[i]);
            }else{
                isAllSelected = !1;
            }
        }

        returnObj.selectedItems = selectedItems;
        returnObj.isAllSelected = isAllSelected;

        return returnObj
    };

    return{
        getFilterSet : getFilterSet
        ,getAllScreenListWithSelectedBool : getAllScreenListWithSelectedBool
        ,getAllPlaylistsListWithSelectedBool : getAllPlaylistsListWithSelectedBool
        ,getAllContentListWithSelectedBool : getAllContentListWithSelectedBool
        ,getSelectedItems : getSelectedItems
    }

}]);

//filters
rApp.directive('filters',[function(){
    /*
        Directive Type : isolate
        Description : This directive provides the filters a user can select and outputs the same
         to fetch the results from those filters. It has properties which can be enabled based on
         the type of reports (screens/playlists/content)

        fields ={
            //Default options
            from_date :
            to_date :
            from_time :
            to_time :

            //on demand (need to be set, in order to avail)
            screens :
            playlists :
            content_files :
        }
    */
    var controllerFunction = ['$scope','filtersFactory','$uibModal',
     function($scope, ff, $uibModal){
        var filtersCtrl = this;

        //get the default filterset here
        var onLoad = function(){
            filtersCtrl.resetFilterset();

            //Call refresh function as
        }

        filtersCtrl.resetFilterset = function(){
            $scope.filterset = ff.getFilterSet($scope.optionalFiltersChoices);
        }

        //filtersUpdate
        filtersCtrl.filterIconClicked = function(){
            var modalInstance = $uibModal.open({
                animation: true
                ,templateUrl: '/static/templates/reports/_filterset_mdl.html'
                ,controller: 'filtersetMdlCtrl'
                ,controllerAs : 'filtersetMdlCtrl'
                ,size: 'lg'
                ,backdrop: 'static' //disables modal closing by click on the backdrop.
                ,resolve: {
                    resolvedData: function(){
                        var resolvedData = {};
                        resolvedData.filterset = $scope.filterset;
                        resolvedData.optionalFiltersChoices = $scope.optionalFiltersChoices;
                        return resolvedData
                    }
                }
            });

            modalInstance.result.then(function filtersUpdated(filterset){
                $scope.filterset = angular.copy(filterset);
                $scope.refreshDataFn()($scope.filterset);
            }, function cancelled(){

            });
        }

        filtersCtrl.clearFilters = function(){
            filtersCtrl.resetFilterset();
        }

        $scope.removeScreens = function(index){
            $scope.filterset.screens.splice(index,1);
        }

        $scope.removePlaylist = function(index){
            $scope.filterset.playlists.splice(index,1);
        }

        $scope.removeContentFile = function(index){
            $scope.filterset.content_files.splice(index,1);
        }


        onLoad();
    }];

    return{
        restrict : 'E'
        ,scope :{
            optionalFiltersChoices : '='
            ,refreshDataFn : '&'
        }
        ,templateUrl : '/static/templates/reports/_filters.html'
        ,controller : controllerFunction
        ,controllerAs : 'filtersCtrl'
    }
}]);

//filtersetMdlCtrl
rApp.controller('filtersetMdlCtrl', ['$scope','resolvedData','$uibModalInstance','filtersFactory','$filter',
function($scope, resolvedData,$uibModalInstance, ff, $filter){
    var filtersetMdlCtrl = this;
    var filter = $filter('filter');

    var onLoad = function(){
        //set the modal's filterset variable
        $scope.filterset = angular.copy(resolvedData.filterset);
        //set the choices
        filtersetMdlCtrl.optionalFiltersChoices = resolvedData.optionalFiltersChoices;
        //set the active tab to 0
        filtersetMdlCtrl.activeTab = 0;

        if(filtersetMdlCtrl.optionalFiltersChoices.screens){
            //get all screen objects with property selected
            ff.getAllScreenListWithSelectedBool($scope.filterset.screens, $scope.filterset.all_screens)
            .then(function(screens){
                filtersetMdlCtrl.screens = screens;
            });
        }
        if(filtersetMdlCtrl.optionalFiltersChoices.playlists){
            //get all playlist objects with property selected
            ff.getAllPlaylistsListWithSelectedBool($scope.filterset.playlists, $scope.filterset.all_playlists)
            .then(function(playlists){
                filtersetMdlCtrl.playlists = playlists;
            });
        }
        if(filtersetMdlCtrl.optionalFiltersChoices.content_files){
            //get all content objects with property selected
            ff.getAllContentListWithSelectedBool($scope.filterset.content_files, $scope.filterset.all_content_files)
            .then(function(content_files){
                filtersetMdlCtrl.content_files = content_files;
            });
        }

    }
    onLoad();

    var validateFilters = function(){
        var valid = true;
        var returnObj = {
            valid : false,
            errMessage : ''
        }
        if($scope.filterDatesForm.$valid){
            returnObj.valid = true;
        }else{
            returnObj['valid'] = false;
            returnObj['errMessage'] += "Inputs are not valid. Please check. "
        }
        return returnObj
    }

    //Date picker options
    filtersetMdlCtrl.startDateOptions = {
            dateDisabled: false,
            formatYear: 'yy',
            maxDate: moment().toDate(),
            minDate: new Date(2016, 01, 01),
            startingDay: 1
            ,showWeeks : false
        };
    filtersetMdlCtrl.endDateOptions = {
            dateDisabled: false,
            formatYear: 'yy',
            maxDate: moment().toDate(),
            minDate: $scope.filterset.start_date,
            startingDay: 1
            ,showWeeks : false
        };
    filtersetMdlCtrl.openDatepicker = function(datetype){
        if(datetype == 'startDate' )
        {
            filtersetMdlCtrl.popUp1.opened = true;
        }
        else
        {
            filtersetMdlCtrl.popUp2.opened = true;
        }
    }
    filtersetMdlCtrl.popUp1 = { opened : false };
    filtersetMdlCtrl.popUp2 = { opened : false };

    filtersetMdlCtrl.navigateToTab = function(index){
        filtersetMdlCtrl.activeTab = index;
    }

    filtersetMdlCtrl.apply = function(){
        var validationCheck = validateFilters();
        if(validationCheck.valid){
            //get only selected screens/playlists/contentFiles
            if(filtersetMdlCtrl.optionalFiltersChoices.screens){
                var returnObj = ff.getSelectedItems(angular.copy(filtersetMdlCtrl.screens));
                $scope.filterset.screens = returnObj.selectedItems;
                $scope.filterset.all_screens = returnObj.isAllSelected;
            }
            if(filtersetMdlCtrl.optionalFiltersChoices.playlists){
                var returnObj = ff.getSelectedItems(angular.copy(filtersetMdlCtrl.playlists));
                $scope.filterset.playlists = returnObj.selectedItems;
                $scope.filterset.all_playlists = returnObj.isAllSelected;
            }
            if(filtersetMdlCtrl.optionalFiltersChoices.content_files){
                var returnObj = ff.getSelectedItems(angular.copy(filtersetMdlCtrl.content_files));
                $scope.filterset.content_files = returnObj.selectedItems;
                $scope.filterset.all_content_files = returnObj.isAllSelected;
            }
            $uibModalInstance.close($scope.filterset)
        }
        else{
            toastr.warning(validationCheck.errMessage);
        }
    }

    filtersetMdlCtrl.cancel = function(){
        $uibModalInstance.dismiss();
    }

}]);

//filtersetTextbox
rApp.directive('filtersetTextbox',[ function(){
    /*
        Directive Type : same scope as parent --> filters
        Description : This directive provides the filters a user can select and outputs the same
         to fetch the results from those filters. It has properties which can be enabled based on
         the type of reports (screens/playlists/content)
    */

    return{
        restrict : 'E'
        ,templateUrl : '/static/templates/reports/_filterset_textbox.html'
    }
}]);

//largerThanDate
rApp.directive("largerThanDate", [function() {
        return {
            require: "ngModel",
            link: function(e, t, n, i) {
                e.$watchGroup(['filterset.start_date', 'filterset.end_date'], function(e) {
                    var startDate = e[0] && new Date(e[0])
                      , endDate = e[1] && new Date(e[1])
                      , r = !(startDate && endDate && startDate > endDate);
                    i.$setValidity("largerThanDate", r)
                })
            }
        }
    }
]);

//largerThanTime
rApp.directive("largerThanTime", [function() {
        return {
            require: "ngModel",
            link: function(e, t, n, i) {
                e.$watchGroup(["filterset.start_time", "filterset.end_time"], function(e) {
                    var startTime = e[0] && new Date(e[0])
                      , endTime = e[1] && new Date(e[1])
                      , r = !(startTime && endTime && startTime >= endTime);
                    i.$setValidity("largerThanTime", r)
                });
            }
        }
    }
]);

//select-all directive
rApp.directive('selectAllCheckbox', function () {
    return {
        replace: true,
        restrict: 'E',
        scope: {
            checkboxes: '=',
            allselected: '=allSelected',
            allclear: '=allClear'
        },
        template: '<input type="checkbox" ng-model="master" ng-change="masterChange()">',
        controller: function ($scope, $element) {

            $scope.masterChange = function () {
                if ($scope.master) {
                    angular.forEach($scope.checkboxes, function (cb, index) {
                        cb.selected = true;
                    });
                } else {
                    angular.forEach($scope.checkboxes, function (cb, index) {
                        cb.selected = false;
                    });
                }
            };

//            $scope.$watch('checkboxes', function () {
//                var allSet = true,
//                    allClear = true;
//                angular.forEach($scope.checkboxes, function (cb, index) {
//                    if (cb.selected) {
//                        allClear = false;
//                    } else {
//                        allSet = false;
//                    }
//                });
//
//                if ($scope.allselected !== undefined) {
//                    $scope.allselected = allSet;
//                }
//                if ($scope.allclear !== undefined) {
//                    $scope.allclear = allClear;
//                }
//
//                $element.prop('indeterminate', false);
//                if (allSet) {
//                    $scope.master = true;
//                } else if (allClear) {
//                    $scope.master = false;
//                } else {
//                    $scope.master = false;
//                    $element.prop('indeterminate', true);
//                }
//
//            }, true);
        }
    };
});

//toggle-selected item
rApp.directive('toggleSelection', function(){
    return{
        restrict : 'A'
        ,scope : {
            item : '='
        }
        ,link : function($scope, elem, attr){
            elem.bind('click', function(e){
                $scope.item.selected = !$scope.item.selected
                $scope.$apply();
            });
        }
    }
})