//This file to maintain Screen and Group (SAG) management

var sagApp = angular.module("sagApp",[]).config(function($interpolateProvider) {
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

    var fieldsData = function(data, idName){
        var returnData = [];
        for( var i=0; i< data.length; i++)
        {
            returnData.push(data[i].fields);
            returnData[i][idName] = data[i].pk;
        }
        return returnData
    }

    var getAllScreens = function(callback){
        $http({
            method : "GET",
            url : "getScreens"
        }).then(function mySucces(response) {
            allScreens = angular.copy(response.data);
            allScreens= fieldsData(allScreens, 'screen_id');
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
            allGroups = fieldsData(allGroups, 'group_id');
            if(callback)
            {
                callback(allGroups);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getGroupScreens = function(group_id, callback){
        console.log(group_id);
        $http({
            method : "GET",
            url : "getScreens/" + group_id
        }).then(function mySucces(response) {
            var data = angular.copy(response.data);
            data = fieldsData(data, 'screen_id');
            if(callback)
            {
                callback(data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    }

    var upsertScreen = function(screenDetails, callback){
        $http({
            method : "POST",
            url : "upsertScreen",
            data : {
                screenDetails : screenDetails
            }
        }).then(function mySucces(response) {
            allScreens = angular.copy(response.data);
            allScreens= fieldsData(allScreens, 'screen_id');
            if(callback)
            {
                callback(allScreens);
            }
            return allScreens
        }, function myError(response) {
            console.log(response.statusText);
        });

    }

    return{
        getAllScreens : getAllScreens,
        getAllGroups : getAllGroups,
        getGroupScreens : getGroupScreens,
        upsertScreen : upsertScreen
    }

}]);

sagApp.factory('screensFactory',['$http', 'dataAccessFactory', function($http, dataAccessFactory){

    var allScreens = [];

    var getAllScreens = function(callback){
        dataAccessFactory.getAllScreens(callback);
    }

    var screenBluePrint = {
        screenId : -1,
        screenName : '',
        address : '',
        aspect_ratio : '',
        screen_size : '',
        activation_key : '',
        resolution :'',
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
    screenBluePrint : screenBluePrint,
    getSelectableGroups : getSelectableGroups
    ,getAllScreens : getAllScreens
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

sagApp.controller('groupCtrl',['groupsFactory', 'dataAccessFactory', '$scope', function(groupsFactory, dataAccessFactory, $scope){

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
        dataAccessFactory.getGroupScreens(group.group_id,function(groupScreens){
            $scope.screensInSelectedGroup = groupScreens;
        });

    }


}]);

sagApp.controller('screenCtrl',['screensFactory','dataAccessFactory', '$scope',  function(screensFactory,dataAccessFactory, $scope){

    var onLoad = function(){
        screensFactory.getAllScreens(function(allScreens)
        {
            $scope.screens = allScreens;
        });
        $scope.isNewScreenModal = false;
    };

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
        dataAccessFactory.upsertScreen($scope.modalScreenDetailsObj, function successFN(upsertStatus){
            if(upsertStatus =='success')
            {
                screensFactory.getAllScreens(function(allScreens)
                {
                    $scope.screens = allScreens;
                });
                toastr.success('Screens details saved');
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

}]);