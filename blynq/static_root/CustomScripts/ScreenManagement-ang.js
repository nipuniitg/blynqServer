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
            url : "getScreens"
        }).then(function mySucces(response) {
            allScreens = angular.copy(response.data);
            if(callback)
            {
                callback(allScreens);
            }
            return allScreens
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getAllGroups = function(callback){
        $http({
            method : "GET",
            url : "getGroups"
        }).then(function mySucces(response) {
            var allGroups = angular.copy(response.data);
            if(callback)
            {
                callback(allGroups);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var upsertScreen = function(screenDetails, callback){
        // var screenDetailsJson = JSON.stringify(screenDetails);
        $http({
            method : "POST"
            ,url : "upsertScreen"
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
            ,url : "upsertGroup"
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

    var getSelectableGroups = function(screen_id, callback){
        $http({
            method : "GET",
            url : "getSelectableGroups/" + screen_id
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getSelectableScreens = function(group_id, callback){
        $http({
            method : "GET",
            url : "getSelectableScreens/" + group_id
        }).then(function mySucces(response) {
            var data = angular.copy(response.data);
            if(callback)
            {
                callback(data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getScreenSchedules  =   function(screen_id, callback){
        $http({
            method : "GET",
            url : "/schedule/getScreenSchedulesJson/" + screen_id
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
            ,url : "deleteGroup"
            ,data : postData
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
        getAllScreens : getAllScreens,
        getAllGroups : getAllGroups,
        upsertScreen : upsertScreen,
        upsertGroup : upsertGroup,
        getSelectableScreens : getSelectableScreens,
        getSelectableGroups : getSelectableGroups
        ,getScreenSchedules :   getScreenSchedules
        ,deleteGroup : deleteGroup
    }

}]);

sagApp.factory('screensFactory',['$http', 'dataAccessFactory', function($http, dataAccessFactory){

    var allScreens = [];

    var getAllScreens = function(callback){
        dataAccessFactory.getAllScreens(callback);
    }

    var screenBluePrint = {
        screen_id : -1,
        screen_name : '',
        address : '',
        aspect_ratio : '',
        screen_size : '',
        activation_key : '',
        resolution :'',
        groups : [],
    }

    return{
    screenBluePrint : screenBluePrint
    ,getAllScreens : getAllScreens
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

sagApp.controller('groupCtrl',['groupsFactory', 'dataAccessFactory', '$scope',
function(groupsFactory, dataAccessFactory, $scope){


   var onLoad = function(){
          refreshGroups();
          $scope.selectedIndex = 0;
          $scope.isNewGroupModal = false;
   }

   var refreshGroups = function(){
        groupsFactory.getAllGroups(function(groups){
                $scope.groups = groups;
          });
   };

   var getSelectableGroups = function(){
        dataAccessFactory.getSelectableScreens($scope.modalGroupDetailsObj.group_id, function(data){
            $scope.selectableScreens = data;
        });
   }


   //add group;
   $scope.addNewGroup = function()
   {
        $scope.modalGroupDetailsObj = angular.copy(groupsFactory.groupBluePrint);
        $scope.isNewGroupModal = true;
        getSelectableGroups();
   };

   $scope.editGroupDetails = function(group, index){
        $scope.modalGroupDetailsObj = angular.copy(group);
        $scope.editModelGroupIndex = index;
        getSelectableGroups();
   };

   $scope.saveGroupDetails = function(){

        dataAccessFactory.upsertGroup($scope.modalGroupDetailsObj, function successFN(data){
            if(data.success)
            {
                refreshGroups();
                if($scope.isNewGroupModal)
                {
                    toastr.success('Group added successfully');
                }
                else{
                    toastr.success('Group updated successfully');
                }
            }
            else{
                toastr.warning("There was some error while adding group. Please try again after sometime.");
            }
            $scope.isNewGroupModal = false;
        });
   };

   $scope.cancelGroupDetailsEdit = function(){
        $scope.isNewGroupModal = false;
   }

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

   $scope.moveScreenToSelectable = function(screen){
        $scope.selectableScreens.push(screen);
        for(var i=0; i< $scope.modalGroupDetailsObj.screens.length; i++)
        {
            var obj = $scope.modalGroupDetailsObj.screens[i];

            if(screen.screen_id == obj.screen_id)
            {
                $scope.modalGroupDetailsObj.screens.splice(i,1);
                break;
            }
        }

   }

   $scope.moveScreenToSelected = function(screen){
        $scope.modalGroupDetailsObj.screens.push(screen);
        for(var i=0; i < $scope.selectableScreens.length; i++)
        {
            var obj = $scope.selectableScreens[i];

            if(screen.screen_id == obj.screen_id)
            {
                $scope.selectableScreens.splice(i,1);
                break;
            }
        }

   }


    //selectable screens and selected screens

    //shcedules
    $scope.clickedOnGroup= function(group, index){
        $scope.selectedIndex = index;
        $scope.screensInSelectedGroup = group.screens;
    }

    onLoad();

}]);

sagApp.controller('screenCtrl',['screensFactory','dataAccessFactory', '$scope',  function(screensFactory,dataAccessFactory, $scope){

    //private functions
    var onLoad = function(){
        screensFactory.getAllScreens(function(allScreens)
        {
            $scope.screens = allScreens;
        });
        $scope.isNewScreenModal = false;
        $scope.activeScreenIndex = 0;
    };

    var setActiveScreenIndex = function(index){
        $scope.activeScreenIndex =index;
    };

    var addGroupsToScreen = function(){
      dataAccessFactory.getSelectableGroups($scope.modalScreenDetailsObj.screen_id, function(selectableGroups)
      {
        $scope.selectableGroups = angular.copy(selectableGroups);
      });
    };


    //public functions
    //screen Details
    $scope.addNewScreen = function(){
        $scope.isNewScreenModal = true;
        $scope.modalScreenDetailsObj = angular.copy(screensFactory.screenBluePrint);
        $scope.newScreenValidationKey = '';
        addGroupsToScreen();
    };

    $scope.editScreenDetails = function(index){
        //copy the object
        $scope.modalScreenDetailsObj = angular.copy($scope.screens[index]);
        $scope.editModeScreenIndex = index;
        addGroupsToScreen();
    };

    $scope.saveScreenDetails = function(){
        dataAccessFactory.upsertScreen($scope.modalScreenDetailsObj, function successFN(data){
            if(data.success)
            {
                screensFactory.getAllScreens(function(allScreens)
                {
                    $scope.screens = allScreens;
                });
                if(isNewScreenModal){
                    toastr.success('New Screen Added');
                }
                else{
                    toastr.success('Screens details updated');
                }
            }
            else{
                toastr.warning('Error occured while saving screen. Please try again.');
            }
            $scope.isNewScreenModal = false;

        });

    };

    $scope.cancelScreenDetailsEdit = function(){
        $scope.isNewScreenModal = false;
    };

    $scope.removeGroupTagforScreen = function(index)
    {
        $scope.modalScreenDetailsObj.groups.splice(index,1);
    }

    //groups

    $scope.moveGroupToSelectable = function(group){
        $scope.selectableGroups.push(group);
        for(var i=0; i< $scope.modalScreenDetailsObj.groups.length; i++)
        {
            var obj = $scope.modalScreenDetailsObj.groups[i];

            if(group.group_id == obj.group_id)
            {
                $scope.modalScreenDetailsObj.groups.splice(i,1);
                break;
            }
        }
    };

    $scope.moveGroupToSelected = function(group){
        $scope.modalScreenDetailsObj.groups.push(group);
        for(var i=0; i< $scope.selectableGroups.length; i++)
        {
            var obj = $scope.selectableGroups[i];

            if(group.group_id == obj.group_id)
            {
                $scope.selectableGroups.splice(i,1);
                break;
            }
        }
    };

    onLoad();

    //schedules
    $scope.clickedOnScreen = function(index){
        setActiveScreenIndex(index);
        $scope.refreshScreenSchedules();
    };

    $scope.refreshScreenSchedules = function(){
        dataAccessFactory.getScreenSchedules($scope.screens[$scope.activeScreenIndex].screen_id, function(returnData){
            $scope.screenSchedules = returnData;
        });
    };

}]);