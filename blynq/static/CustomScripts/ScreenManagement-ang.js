//This file to maintain Screen and Group (SAG) management

var sagApp = angular.module("sagApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

//Any methods which touches the dataBase goes here
sagApp.factory('dataAccessFactory', ['$http', function($http){

    var getAllScreens = function(callback){
        $http({
            method : "GET",
            url : "getScreensJson"
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
            url : "getGroupsJson"
        }).then(function mySucces(response) {
            var allGroups = angular.copy(response.data);
            if(callback)
            {
                callback(allGroups);
            }
            return allGroups;
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    return{
        getAllScreens : getAllScreens,
        getAllGroups : getAllGroups
    }

}]);

sagApp.factory('screensFactory',['$http', 'dataAccessFactory', function($http, dataAccessFactory){

    var screens = [{screenId : 1, screenName : 'ScreenName1', groups : [{groupId : 1, groupName : "Shopping Mall"},{groupId : 2, groupName : "supermarket"}], status : 'online', city : 'Hyderabad', resolution : '42*34', company : 'ola'},
    {screenId : 1, screenName : 'secondName', groups : [{groupId : 3, groupName : "cinimax"},{groupId : 4, groupName : "sports corner"}], status : 'online', city : 'Delhi', resolution : '23*44', company : 'oyo'},
    {screenId : 1, screenName : 'third', groups : [{groupId : 5, groupName : "top floor"},{groupId : 6, groupName : "Entrance"}], status : 'online', city : 'Bangalore', resolution : '52*10', company : 'foodpanda'},
    {screenId : 1, screenName : 'random', groups : [{groupId :2, groupName : "supermarket"},{groupId : 3, groupName : "cinimax"}], status : 'online', city : 'Chennai', resolution : '34*25', company : 'ola'},
    {screenId : 1, screenName : 'abby', groups : [{groupId : 7, groupName : "sports center"},{groupId : 0, groupName : "topfloor"}], status : 'online', city : 'Kodai', resolution : '42*23', company : 'swiggy'}
     ];

    var allScreens = [];

    var getAllScreens = function(callback){
        dataAccessFactory.getAllScreens(callback);
    }

    var screenBluePrint = {
        screenId : -1,
        screenName : 'DummyScreenName',
        city : 'Dummy City',
        resolution : '',
        company : '',
        groups : [],
    }

    var getSelectableGroups = function(selectedGroups, callback){
        var selectedGroupIds = [];
        for(var i=0; i<selectedGroups.length; i++)
        {
            selectedGroupIds.push(selectedGroups[i].groupId);
        }

        var allGroups = [];
        dataAccessFactory.getAllGroups(function(groups){
            allGroups = groups;

        var selectableGroups = angular.copy(allGroups);
            for(var i = selectableGroups.length-1; i>-1; i--)
            {
                var obj = selectableGroups[i];
                if(selectedGroupIds.indexOf(obj.groupId) > -1)
                {
                    selectableGroups.splice(i,1);
                }
            }
            callback(selectableGroups);
        });
    };

    return{
    screens : screens,
    screenBluePrint : screenBluePrint,
    getSelectableGroups : getSelectableGroups
    };

}]);

sagApp.factory('groupsFactory',['$http','dataAccessFactory', function($http, dataAccessFactory){

    var groupBluePrint = {
        groupId : -1,
        groupName : "",
        Description : ""
    };

    var allGroups =[];

    var getAllGroups = function(callback){
        dataAccessFactory.getAllGroups(callback);
    };

    var getSelectableScreens = function(selectedScreens, callback){
        var selectedScreenIds = [];
        for(var i=0; i<selectedScreen.length; i++)
        {
            selectedScreenIds.push(selectedScreenIds[i].screenId);
        }

        var allScreens = [];
        dataAccessFactory.getAllScreens(function(screens){
            allScreens = screens;

        var selectableScreens = angular.copy(allScreens);
        for(var i = selectableScreens.length; i>-1; i--)
        {
            var obj = selectableScreens[i];
            if(selectedScreenIds.indexOf(obj.screenId) > -1)
            {
                selectableScreens.splice(i,1);
            }
        }
        callback(selectableGroups);
        });
    };

    return{
        groupBluePrint: groupBluePrint,
        getAllGroups: getAllGroups,
        getSelectableScreens : getSelectableScreens
    };
}]);

sagApp.controller('groupCtrl',['groupsFactory', '$scope', function(groupsFactory, $scope){

   groupsFactory.getAllGroups(function(groups){
            $scope.groups = groups;
   });

   $scope.selectedIndex = 0;
   $scope.isNewGroupModal = false;

   //add group;
   $scope.addNewGroup = function()
   {
        $scope.modalGroupDetailsObj = angular.copy(groupsFactory.groupBluePrint);
        $scope.isNewGroupModal = true;
        groupsFactory.getSelectableScreens($scope.modalGroupDetailsObj.screens, function(data){
            $scope.selectableScreens = data;
        });
   };

   $scope.editGroupDetails = function(group, index){
        $scope.modalGroupDetailsObj = angular.copy(group);
        $scope.editModelGroupIndex = index;
        groupsFactory.getSelectableScreens($scope.modalGroupDetailsObj.screens, function(data){
            $scope.selectableScreens = data;
        });
   };

   $scope.saveGroupDetails = function(){
        if($scope.isNewGroupModal){

        }
        else{
            $scope.groups[$scope.editModelGroupIndex] = angular.copy($scope.modalGroupDetailsObj);
        }

        $scope.isNewGroupModal = false;
   }

   $scope.cancelGroupDetailsEdit = function(){
        $scope.isNewGroupModal = false;
   }

   $scope.moveScreenToSelectable = function(screen){
        $scope.selectableScreens.push(screen);
        for(var i=0; i< $scope.modalGroupDetailsObj.screens.length; i++)
        {
            var obj = $scope.modalGroupDetailsObj.screens[i];

            if(group.groupId == obj.groupId)
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

            if(screen.screenId == obj.screenId)
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
    }


}]);

sagApp.controller('screenCtrl',['screensFactory', '$scope',  function(screensFactory, $scope){

    $scope.screens = screensFactory.screens;
    $scope.isNewScreenModal = false;

    //screen Details
    $scope.addNewScreen = function(){
        $scope.isNewScreenModal = true;
        $scope.modalScreenDetailsObj = angular.copy(screensFactory.screenBluePrint);
        $scope.newScreenValidationKey = '';
    };

    $scope.editScreenDetails = function(index){
        //copy the object
        $scope.modalScreenDetailsObj = angular.copy($scope.screens[index]);
        $scope.editModeScreenIndex = index;
    };

    $scope.saveScreenDetails = function(){
         if($scope.modalScreenDetailsObj.screenId == -1)
         {

         }
         else{
            $scope.screens[$scope.editModeScreenIndex] = angular.copy($scope.modalScreenDetailsObj);
         }

        $scope.isNewScreenModal = false;
        toastr.success('Screens details saved');
    };

    $scope.cancelScreenDetailsEdit = function(){
        $scope.isNewScreenModal = false;
    };

    //groups
    $scope.addGroupsToScreen = function(){
          screensFactory.getSelectableGroups($scope.modalScreenDetailsObj.groups, function(selectableGroups)
          {
            $scope.selectableGroups = angular.copy(selectableGroups);
          });
    };

    $scope.moveGroupToSelectable = function(group){
        $scope.selectableGroups.push(group);
        for(var i=0; i< $scope.modalScreenDetailsObj.groups.length; i++)
        {
            var obj = $scope.modalScreenDetailsObj.groups[i];

            if(group.groupId == obj.groupId)
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

            if(group.groupId == obj.groupId)
            {
                $scope.selectableGroups.splice(i,1);
                break;
            }
        }
    };

    //schedules

}]);