//This file to maintain Screen and Group (SAG) management

var sagApp = angular.module("sagApp",['sdApp']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

sagApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

//Any methods which touches the dataBase goes here
sagApp.factory('dataAccessFactory', ['$http', function($http){

    var getAllScreens = function(callback){
        $http({
            method : "GET",
            url : "/api/screen/getScreens"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getAllGroups = function(callback){
        $http({
            method : "GET",
            url : "/api/screen/getGroups"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var upsertScreen = function(screenDetails, callback){
        // var screenDetailsJson = JSON.stringify(screenDetails);
        $http({
            method : "POST"
            ,url : "/api/screen/upsertScreen"
            ,data : screenDetails
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });

    }

    var upsertGroup = function(groupDetails, callback){
        $http({
            method : "POST"
            ,url : "/api/screen/upsertGroup"
            ,data : groupDetails
            /*data : {
                groupDetails : groupDetails
            }*/
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getScreenSchedules  =   function(screen_id, callback){
        $http({
            method : "GET",
            url : "/api/schedule/getScreenSchedules/" + screen_id
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getGroupSchedules  =   function(group_id, callback){
        $http({
            method : "GET",
            url : "/api/schedule/getGroupSchedules/" + group_id
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var deleteGroup = function(group_id, callback){
        var postData = {
            group_id : group_id
        }
        $http({
            method : "POST"
            ,url : "/api/screen/deleteGroup"
            ,data : postData
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });

    };

    var getCityOptions = function(callback){
        $http({
            method : "GET",
            url : "/api/screen/getCityOptionsJson"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getScreenEvents = function(screen_id, month, callback){
        var postData = {
            screen_id : screen_id
            ,month : month
        }
        $http({
            method : "GET"
            ,url : "/api/schedule/getScreenEvents"
            ,params : postData
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    }

    var getGroupEvents = function(group_id, month, callback){
        var postData = {
            group_id : group_id
            ,month : month
        };
        $http({
            method : "GET"
            ,url : "/api/schedule/getGroupEvents"
            ,params : postData
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    }

    return{
        getAllScreens : getAllScreens
        ,getAllGroups : getAllGroups
        ,upsertScreen : upsertScreen
        ,upsertGroup : upsertGroup
        ,getScreenSchedules :   getScreenSchedules
        ,getGroupSchedules : getGroupSchedules
        ,deleteGroup : deleteGroup
        ,getCityOptions : getCityOptions
        ,getScreenEvents : getScreenEvents
        ,getGroupEvents : getGroupEvents
    }

}]);

sagApp.factory('screensFactory',['$http', 'dataAccessFactory', function($http, dataAccessFactory){

    var allScreens = [];

    var getAllScreens = function(callback){
        dataAccessFactory.getAllScreens(callback);
    };

    var screenBluePrint = {
        screen_id : -1
        ,screen_name : ''
        ,address : ''
        ,aspect_ratio : ''
        ,screen_size : ''
        ,activation_key : ''
        ,resolution :''
        ,city : {
        }
        ,groups : []
    };

    var selectedBoolSetter = function(allItems, selectedItems, key, schedule_key_id){
        var r = []
        ,allItemsLength = allItems.length;

        if (typeof(selectedItems) !== 'undefined'){
            selectedItemsLength = selectedItems.length;
        }
        for(i=0; i<allItemsLength; i++){
            var item = allItems[i];
            if(typeof(selectedItemsLength) !== 'undefined')
            {
                for(l=0; l<selectedItemsLength; l++){
                if(item[key] == selectedItems[l][key]){
                    //set selected bool
                    item['selected']= !0;
                    //set schedule_key_id value from the selected values
                    if(schedule_key_id){
                        item[schedule_key_id] = selectedItems[l][schedule_key_id];
                    }
                    selectedItemsLength -= 1;
                    selectedItems.splice(l,1);
                    break;
                }
                }
            }
            if(!item['selected']){
                item['selected'] = !1;
                //set the new schedule_key_id(schedule_playlist_id, schedule_screen_id, schedule_group_id) as -1
                if(schedule_key_id){
                    item[schedule_key_id] = -1;
                }
            }
            r.push(item);
        }
        return r;
    };



    var getGroupsWithSelectedBool = function(selectedGroups, callback){
        dataAccessFactory.getAllGroups(function(returnData){
            var allGroupsWithSelectedBool = selectedBoolSetter(returnData, selectedGroups, 'group_id','group_screen_id');
            callback(allGroupsWithSelectedBool);
        });
    };

    var getScreensWithSelectedBool = function(selectedGroups, callback){
        dataAccessFactory.getAllScreens(function(returnData){
            var allGroupsWithSelectedBool = selectedBoolSetter(returnData, selectedGroups, 'screen_id', 'group_screen_id');
            callback(allGroupsWithSelectedBool);
        });
    };

    var getSelectedItems = function(allItems){
        var selectedItems = [];
        var allItemsLength = allItems.length;
        for(i=0; i<allItemsLength; i++){
            if(allItems[i].selected){
                delete allItems[i].selected;
                selectedItems.push(allItems[i]);
            }
        }
        return selectedItems;
    };


    return{
    screenBluePrint : screenBluePrint
    ,getAllScreens : getAllScreens
    ,getGroupsWithSelectedBool : getGroupsWithSelectedBool
    ,getScreensWithSelectedBool : getScreensWithSelectedBool
    ,getSelectedItems : getSelectedItems
    };

}]);

sagApp.factory('groupsFactory',['$http','dataAccessFactory', function($http, dataAccessFactory){

    var groupBluePrint = {
        group_id : -1,
        group_name : "",
        description : "",
        screens : []
    };

    var allGroups =[];

    var getAllGroups = function(callback){
        dataAccessFactory.getAllGroups(callback);
    };

    return{
        groupBluePrint: groupBluePrint
        ,getAllGroups: getAllGroups
    };
}]);

//group Index Cntrl
sagApp.controller('groupCtrl',['groupsFactory', 'dataAccessFactory', '$scope','$uibModal','constantsAndDefaults',
function(groupsFactory, dataAccessFactory, $scope,$uibModal, cAD){

   var onLoad = function(){
      refreshGroups();
      setActiveGroupIndex(0);
      $scope.schedulesView = cAD.defaultSchedulesLayoutType();

      //popOver Messages
      $scope.popOverMessages = cAD.getPopOverMessages();
   }

   var setActiveGroupIndex = function(index){
        $scope.activeGroupIndex = index;
   }

   var refreshGroups = function(){
        groupsFactory.getAllGroups(function(groups){
                $scope.groups = groups;
                $scope.refreshGroupSchedulesAndEvents();
          });
   };

   $scope.deleteGroup = function(index){
        dataAccessFactory.deleteGroup($scope.groups[index].group_id, function(responseData){
            if(responseData.success){
                toastr.success('Group deleted successfully');
                refreshGroups();
            }
            else{
                toastr.warning('Oops!. There was some error while deleting group. Please refresh again and try.')
            }
        });
   }

    //shcedules
    $scope.clickedOnGroup= function(group, index){
        setActiveGroupIndex(index);
        $scope.screensInSelectedGroup = group.screens;
        $scope.refreshGroupSchedulesAndEvents();
    }

    $scope.refreshGroupSchedulesAndEvents = function(){
        var currentMonth = moment().month() + 1;
        $scope.refreshGroupSchedules();
        $scope.refreshGroupEvents(currentMonth);
    }

    $scope.refreshGroupSchedules = function(){
        if($scope.groups){
            dataAccessFactory.getGroupSchedules($scope.groups[$scope.activeGroupIndex].group_id, function(returnData){
                $scope.groupSchedules = returnData;
            });
        }else{
            $scope.groupSchedules =0;
        }
    };

    $scope.refreshGroupEvents = function(month){
        dataAccessFactory.getGroupEvents($scope.groups[$scope.activeGroupIndex].group_id,month, function(returnData){
                $scope.groupEvents = returnData;
            });
    }



    //add and Edit Group Details
    var newGroupIndex = -1

    $scope.addNewGroup = function(){
        openGroupDetailsMdl(newGroupIndex);
    }

    $scope.editGroupDetails = function(index){
        openGroupDetailsMdl(index);
    }

    var openGroupDetailsMdl = function(index){
        var isNewGroup = index == newGroupIndex ? !0 : !1;
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/screen/_group_details_mdl.html'
              ,controller: 'mdlUpsertGroupDetails'
              ,size: 'lg'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve: {
                groupDetailsObj: function(){
                    if(isNewGroup)
                    {
                        return angular.copy(groupsFactory.groupBluePrint);
                    }
                    else{
                        return angular.copy($scope.groups[index]);
                    }
                }
              }
        });

        modalInstance.result.then(function saved(){
            refreshGroups();
        }, function cancelled(){
            toastr.warning('Screen Update cancelled')
        })
    };

    onLoad();

}]);

//screen Index Cntrl
sagApp.controller('screenCtrl',['screensFactory','dataAccessFactory', '$scope','$uibModal','constantsAndDefaults',
  function(screensFactory,dataAccessFactory, $scope, $uibModal, cAD){

    //private functions
    var onLoad = function(){
        $scope.refreshScreens();
        $scope.activeScreenIndex = 0;
        //Intialising default view of schedules as list view
        $scope.schedulesView = cAD.defaultSchedulesLayoutType();

        //popOverMessages
        $scope.popOverMessages = cAD.getPopOverMessages();
    };

    var setActiveScreenIndex = function(index){
        $scope.activeScreenIndex =index;
    };


    //public functions
     $scope.refreshScreens = function(){
        screensFactory.getAllScreens(function(allScreens)
        {
            $scope.screens = allScreens;
            $scope.refreshScreenSchedulesandEvents();
        });
     }

    onLoad();

    //schedules
    $scope.clickedOnScreen = function(index){
        setActiveScreenIndex(index);
        $scope.refreshScreenSchedulesandEvents();
    };

    $scope.refreshScreenSchedulesandEvents = function(){
        var currentMonth = moment().month() + 1;
        $scope.refreshScreenSchedules();
        $scope.refreshScreenEvents(currentMonth);
    }

    $scope.refreshScreenSchedules = function(){
        dataAccessFactory.getScreenSchedules($scope.screens[$scope.activeScreenIndex].screen_id, function(returnData){
            $scope.screenSchedules = returnData;
        });
    };

    $scope.refreshScreenEvents = function(month){
        dataAccessFactory.getScreenEvents($scope.screens[$scope.activeScreenIndex].screen_id,month,function(returnData){
            $scope.screenEvents = returnData;
        });
    }


    //add and Edit Screen Details
    var newScreenIndex = -1

    $scope.addNewScreen = function(){
        openScreenDetailsMdl(newScreenIndex);
    }

    $scope.editScreenDetails = function(index){
        openScreenDetailsMdl(index);
    }

    var openScreenDetailsMdl = function(index){
        var isNewScreen = index == newScreenIndex ? !0 : !1;
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/screen/_screen_details_mdl.html'
              ,controller: 'mdlUpsertScreenDetails'
              ,size: 'lg'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve: {
                screenDetailsObj: function(){
                    if(isNewScreen)
                    {
                        return angular.copy(screensFactory.screenBluePrint);
                    }
                    else{
                        return angular.copy($scope.screens[index]);
                    }
                }
              }
        });

        modalInstance.result.then(function saved(){
            $scope.refreshScreens();
        }, function cancelled(){
            toastr.warning('Screen Update cancelled')
        })
    };
}]);

//upsertScreenDetails
sagApp.controller('mdlUpsertScreenDetails', ['$scope','$uibModalInstance','screenDetailsObj','dataAccessFactory',
'$uibModal', function($scope,$uibModalInstance, screenDetailsObj,dAF,$uibModal){

    var isNewScreen = screenDetailsObj.screen_id == -1 ? !0 : !1;

    var onLoad= function(){
        $scope.screenDetails = screenDetailsObj;
        $scope.showActivationKeyField = isNewScreen ? !0 : !1;
        $scope.saveButtonVerbose = isNewScreen ? 'Add' : 'Update';
        dAF.getCityOptions(function(returnData){
            $scope.cityOptions = returnData;
        });
    };

    $scope.validateActivationKey = function(){

    };

    $scope.removeGroup = function(index){
        $scope.screenDetails.groups.splice(index,1);
    }

    $scope.openGroupSelectorModal = function(){
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/static/templates/screen/_group_selection_mdl.html',
          controller: 'mdlGroupSelectionCtrl',
          size: 'lg'
          ,backdrop: 'static' //disables modal closing by click on the backdrop.
          ,resolve: {
            selectedGroups : function(){
                return angular.copy($scope.screenDetails.groups)
            }
          }
        });

        modalInstance.result.then(function apply(selectedGroups){
            $scope.screenDetails.groups = angular.copy(selectedGroups);
        }, function cancel(){
            toastr.warning('cancelled');
        })
    };

    $scope.upsertScreen = function(){
        console.log($scope.screenDetails)
        dAF.upsertScreen($scope.screenDetails, function(returnData){
            if(returnData.success){
                if(isNewScreen){
                    toastr.success('Screen added successfully');
                }
                else{
                    toastr.success('Screen updated successfully.')
                }
                $uibModalInstance.close();
            }
            else{
                toastr.warning('Oops! There was some error while updating the details. Please try again later.')
            }
        });
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss();
    }

    onLoad();
}]);
//upsert Group Details
sagApp.controller('mdlUpsertGroupDetails',['$scope','$uibModalInstance', 'groupDetailsObj', 'dataAccessFactory',
 '$uibModal',function($scope,$uibModalInstance, groupDetailsObj,dAF,$uibModal){

    var isNewGroup = groupDetailsObj.group_id == -1 ? !0 : !1;

    var onLoad= function(){
        $scope.groupDetails = groupDetailsObj;
        $scope.saveButtonVerbose = (isNewGroup) ? 'Add' : 'Update'
    };

    $scope.openScreenSelectorModal = function(){
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/static/templates/screen/_screen_selection_mdl.html',
          controller: 'mdlScreenSelectionCtrl',
          size: 'lg'
          ,backdrop: 'static' //disables modal closing by click on the backdrop.
          ,resolve: {
            selectedScreens : function(){
                return angular.copy($scope.groupDetails.screens)
            }
          }
        });

        modalInstance.result.then(function apply(selectedScreens){
            $scope.groupDetails.screens = angular.copy(selectedScreens);
        }, function cancel(){
            toastr.warning('cancelled');
        })
    };

    $scope.removeScreen = function(index){
        $scope.groupDetails.screens.splice(index,1);
    }

    $scope.upsertGroup = function(){
        console.log()
        dAF.upsertGroup($scope.groupDetails, function successFN(data){
            if(data.success)
            {
                if(isNewGroup)
                {
                    toastr.success('Group added successfully');
                }
                else{
                    toastr.success('Group updated successfully');
                }
                $uibModalInstance.close();
            }
            else{
                toastr.warning("There was some error while adding group. Please try again after sometime.");
            }
        });
    };

    $scope.cancel=function(){
        $uibModalInstance.dismiss();
    }

    onLoad();

 }]);


//ScreenDetails-mdlGroupSelectionCntrl
sagApp.controller('mdlGroupSelectionCtrl',['$scope','$uibModalInstance', 'selectedGroups','screensFactory',
 function($scope, $uibModalInstance, selectedGroups,sF){

    var onLoad = function(){
        sF.getGroupsWithSelectedBool(selectedGroups, function(returnData){
            $scope.allGroups = returnData
        });
    };

    $scope.update = function(){
        var selectedGroups = sF.getSelectedItems($scope.allGroups);
        $uibModalInstance.close(selectedGroups);
    }

    $scope.cancel =function(){
        $uibModalInstance.dismiss();
    }

    onLoad();


}]);

//GroupDetails-mdlScreenSelection
sagApp.controller('mdlScreenSelectionCtrl',['$scope','$uibModalInstance', 'selectedScreens','screensFactory',
 function($scope, $uibModalInstance, selectedScreens,sF){

    var onLoad = function(){
        sF.getScreensWithSelectedBool(selectedScreens, function(returnData){
            $scope.allScreens = returnData
        });
    };

    $scope.update = function(){
        var selectedScreens = sF.getSelectedItems($scope.allScreens);
        $uibModalInstance.close(selectedScreens);
    }

    $scope.cancel =function(){
        $uibModalInstance.dismiss();
    }

    onLoad();


}]);




