/*var ctApp = angular.module('ctApp',['as.sortable']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });*/

plApp.factory('ctDataAccessFactory',['$http','$window', function($http,$window){

    var getContentJson = function(callback){
        var URL = '/content/getContentJson';
        $http({
             method : "GET",
             url : URL
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    //How to send data to views through ajax in django
    var deleteContent = function(content, callback){
        $http({
             method : "POST"
             ,url : '/content/deleteContent'
             ,data : content
         }).then(function mySuccess(response){
                var returnData = response.data;
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var getFilesJson = function(folderId, callback){
        var URL = '/content/getFilesJson/'+ folderId;
        $http({
             method : "GET",
             url : URL
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var getFoldersJson = function(folderId, callback){
        var URL = '/content/getFoldersJson/'+ folderId;
        $http({
             method : "GET",
             url : URL
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var uploadContent = function(file, currentFolderId, newContentObj, callback){
        var fd = new FormData();
        fd.append('file', file);
        fd.append('title', newContentObj.title);
        fd.append('currentFolderId', currentFolderId);
        uploadUrl ='/content/uploadContent'
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        }).then(function mySuccess(response){
                var returnData = response.data;
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var createFolder = function(currentFolderId, mdlObj, callback){
        postData ={};
        postData.currentFolderId = currentFolderId;
        postData.title = mdlObj.title;
        $http({
             method : "POST",
             url : '/content/createFolder',
             data : postData
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var updateContentTitle = function(contentObj, callback){
        $http({
             method : "POST",
             url : '/content/updateContentTitle',
             data : contentObj
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var getFolderPath = function(folderId, callback){
        $http({
             method : "GET"
             ,url : '/content/folderPath/'+ folderId
         }).then(function mySuccess(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    return{
        getContentJson : getContentJson
        ,deleteContent : deleteContent
        ,getFiles : getFilesJson
        ,getFolders : getFoldersJson
        ,uploadContent : uploadContent
        ,createFolder : createFolder
        ,updateContentTitle : updateContentTitle
        ,getFolderPath : getFolderPath
    }

}]);

//Any logic that needs some computation goes here.
plApp.factory('ctFactory', ['ctDataAccessFactory', function(ctDataAccessFactory){

    // These are used by the playlist controller.
    var folders =null;
    var files = null;


    var getFolders = function(folderId, callback)
    {
        ctDataAccessFactory.getFolders(folderId,function(data)
        {
            folders = data;
            callback(data)
        });
    };

    var getFiles = function(folderId, callback)
    {
        ctDataAccessFactory.getFiles(folderId,function(data)
        {
            files = data;
            callback(data)
        });
    };

    var getFoldersObj = function()
    {
        return folders;
    };

    var getFilesObj = function()
    {
        return files;
    };

    return{
        getFolders : getFolders
        ,getFiles : getFiles
        ,getFoldersObj : getFoldersObj
        ,getFilesObj : getFilesObj
    }

}]);

plApp.controller('ctCtrl',['$scope','ctFactory','ctDataAccessFactory', function($scope, ctFactory, ctDataAccessFactory){

    //private functions
    var onLoad = function(){
        $scope.currentFolderId = -1  //-1 represents root folder. And hence fetches the data in root folder.
        refreshContent($scope.currentFolderId);
        updateFolderPath($scope.currentFolderId);
    };

    var refreshContent = function(folderId){

        ctFactory.getFolders(folderId, function(data)
        {
            $scope.folders = data;
        });

        ctFactory.getFiles(folderId, function(data)
        {
            $scope.files = data;
        });

    };

    var updateFolderPath = function(folderId){
        ctDataAccessFactory.getFolderPath(folderId, function(data){
            $scope.folderPath = data
            $scope.currentFolderId = folderId;
        });

    }



    //public or Scope releated functions
    $scope.deleteContent = function(content){
        ctDataAccessFactory.deleteContent(content,  function(data){
            if(data.success)
            {
                refreshContent($scope.currentFolderId);
                toastr.success('Item deleted successfully.');
            }
            else{
                toastr.warning("Oops!!There was some error. Please try later.");
            }
        });
    }

    $scope.upload = function(){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        ctDataAccessFactory.uploadContent(file, $scope.currentFolderId, $scope.mdlNewFileDetailsObj, function(data){
            if(data.success){
                refreshContent($scope.currentFolderId);
                toastr.success('Upload successful');
            }
            else{
                toastr.warning('Upload failed. Please try after some time.');
            }
        });
    }

    $scope.navigateToFolder = function(folderId){
        refreshContent(folderId);
        updateFolderPath(folderId);
    }

    //----createFolderfunctions
    var clearCreateFolderModalObj = function(){
        $scope.mdlNewFolderObj.title = '';
    }

    $scope.cancelCreateFolder = function()
    {
        clearCreateFolderModalObj();
    }

    $scope.createFolder = function(){
        ctDataAccessFactory.createFolder($scope.currentFolderId, $scope.mdlNewFolderObj, function(data){
            if(data.success)
            {
                refreshContent($scope.currentFolderId);
                toastr.success('Folder created Successfully');
            }
            else{
                toastr.warning('Oops!!There was some error while creating folder. Please try again.');
            }
            clearCreateFolderModalObj();
        });
    }
    //----createFolderfunctions


    //----editContentTitle

    $scope.editTitle= function(content){
        $scope.mdlEditContentObj = angular.copy(content);
    }

    $scope.updateContentTitle= function(){
        ctDataAccessFactory.updateContentTitle($scope.mdlEditContentObj, function(data){
            if(data.success)
            {
                refreshContent($scope.currentFolderId);
                toastr.success('Title Modified successfully');
            }
            else{
                toastr.warning('Oops!! Some error occured while updating the template');
            }
        });
    }

    $scope.cancelupdateContentTitle = function(){
        $scope.mdlEditContentObj = null;
    }

    //----

    onLoad();
}]);

plApp.directive('draggable', function(){
return{
    restrict : 'A',
    link: function(scope, element, attrs) {
        element.draggable({
            revert : 'invalid'
            ,helper: 'clone'
            /*,containment : 'section.wrapper'*/
            ,stack : '.div-draggable-wrap'
            ,snap : '#ul-playlistQueue'
            ,zIndex : 50000
            ,start : function(event, ui){
            }
            ,stop : function(event,ui){
            }
        });
        }
}});

plApp.directive('droppable', function(){
return{
    restrict : 'A'
    ,scope : {
        addContentFunction : '&addContentFunction'
        ,addFolderFunction : '&addFolderFunction'
    }
    ,link: function(scope, element, attrs) {
            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : '.highlight-acceptable'
              ,drop: function(event, ui){

                   var dragIndex = angular.element(ui.draggable).data('index');
                   var isFolder = angular.element(ui.draggable).data('isfolder');
                   if(isFolder){
                        scope.addFolderFunction()(dragIndex);
                   }
                   else
                   {
                        scope.addContentFunction()(dragIndex);
                   }

                }
            });

        }
}});

plApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);