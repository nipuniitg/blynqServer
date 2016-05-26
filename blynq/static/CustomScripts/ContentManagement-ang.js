/*var ctApp = angular.module('ctApp',['as.sortable']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });*/

plApp.factory('ctDataAccessFactory',['$http','$window', function($http,$window){

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
    };

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
    };

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
    };

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
    };

    var moveContent = function(content_ids, parent_folder_id, callback){
        var postData ={
            content_ids : content_ids
            ,parent_folder_id : parent_folder_id
        };
        $http({
             method : "POST",
             url : '/content/moveContent',
             data : postData
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    return{
        deleteContent : deleteContent
        ,getFiles : getFilesJson
        ,getFolders : getFoldersJson
        ,uploadContent : uploadContent
        ,createFolder : createFolder
        ,updateContentTitle : updateContentTitle
        ,getFolderPath : getFolderPath
        ,moveContent    :   moveContent
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

plApp.controller('ctCtrl',['$scope','ctFactory','ctDataAccessFactory', '$uibModal',
function($scope, ctFactory, ctDataAccessFactory, $uibModal){

    //private functions
    var onLoad = function(){
        $scope.currentFolderId = -1  //-1 represents root folder. And hence fetches the data in root folder.
        $scope.refreshContent($scope.currentFolderId);
    };

    $scope.refreshContent = function(folderId){

        ctFactory.getFolders(folderId, function(data)
        {
            $scope.folders = data;
        });

        ctFactory.getFiles(folderId, function(data)
        {
            $scope.files = data;
        });

        clearCheckedLists();

        updateFolderPath(folderId);

    };

    var updateFolderPath = function(folderId){
        ctDataAccessFactory.getFolderPath(folderId, function(data){
            $scope.folderPath = data
            $scope.currentFolderId = folderId;
        });
    };



    //public or Scope releated functions
    $scope.deleteContent = function(content){
        ctDataAccessFactory.deleteContent(content,  function(data){
            if(data.success)
            {
                $scope.refreshContent($scope.currentFolderId);
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
                $scope.refreshContent($scope.currentFolderId);
                toastr.success('Upload successful');
            }
            else{
                toastr.warning('Upload failed. Please try after some time.');
            }
        });
    }

    $scope.navigateToFolder = function(folderId){
        $scope.refreshContent(folderId);
    };

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
                $scope.refreshContent($scope.currentFolderId);
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
                $scope.refreshContent($scope.currentFolderId);
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

    //move item
    var clearCheckedLists = function(){
        $scope.checkedFolders = [];
        $scope.checkedContent =[];
    }

    $scope.toggleCheck = function(type, index){
        if(type=='folder'){
            var idx = $scope.checkedFolders.indexOf(index)
            if (idx > -1) {
              $scope.checkedFolders.splice(idx, 1);
            }

            // is newly selected
            else {
              $scope.checkedFolders.push(index);
            }
        }
        else{
            var idx = $scope.checkedContent.indexOf(index)
            if (idx > -1) {
              $scope.checkedContent.splice(idx, 1);
            }

            // is newly selected
            else {
              $scope.checkedContent.push(index);
            }
        }
    }

    $scope.moveContent = function(){
        if($scope.checkedFolders.length > 0 || $scope.checkedContent.length >0)
        {
            var content_ids =[];
            for(i=0;i<$scope.checkedFolders.length;i++)
            {
                content_ids.push($scope.folders[$scope.checkedFolders[i]].content_id);
            }
            for(i=0;i<$scope.checkedContent.length;i++)
            {
                content_ids.push($scope.files[$scope.checkedContent[i]].content_id);
            }
            var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/templates/contentManagement/_folders_list_mdl.html'
              ,controller: 'mdlContentMoveCtrl'
              ,size: 'lg'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    content_ids : function(){
                        return content_ids
                    }
              }
            });

            modalInstance.result.then(function moveTo(newParentId){
                ctDataAccessFactory.moveContent(content_ids, newParentId, function(returnData){
                    toastr.success('Content Moved Successfully.');
                    $scope.refreshContent($scope.currentFolderId);
                });
            }, function cancelled(){
                toastr.warning('Move cancelled')
            });
        }
        else{
            toastr.warning('Check atleast one item to complete the action')
        }
    };


    //view Content
    $scope.viewContentInDetail = function(file){
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/templates/contentManagement/_content_view_mdl.html'
              ,controller: 'contentInDetailMdlCtrl'
              ,size: 'lg'
              //,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    file : function(){
                        return file
                    }
              }
            });

        modalInstance.result.then(function ok(newParentId){

        }, function cancelled(){

        });
    }

    onLoad();
}]);

plApp.controller('mdlContentMoveCtrl', ['content_ids','$scope','$uibModalInstance','ctDataAccessFactory',
 function(content_ids,$scope,$uibModalInstance, ctDAF){

    var onLoad = function(){
        $scope.currentFolderId = -1;
        refreshFolders($scope.currentFolderId);
        updateFolderPath($scope.currentFolderId);
    };

    var refreshFolders = function(content_id){
        ctDAF.getFolders(content_id, function(returnData){
            $scope.folders = returnData;
        });
    };

    var updateFolderPath = function(folderId){
        ctDAF.getFolderPath(folderId, function(data){
            $scope.folderPath = data
            $scope.currentFolderId = folderId;
        });
    };

    $scope.navigateToFolder = function(folderId){
        refreshFolders(folderId);
        updateFolderPath(folderId);
    };

    var validateErrors = function(){
        var idx = content_ids.indexOf($scope.currentFolderId);
        if(idx > -1)
        {
            return true
        }
        else{
            return false
        }
    }

    $scope.moveHere = function(){
        if(validateErrors()){
            toastr.error('You are trying to move folder into itself. Please re-check');
        }
        else{
            toastr.success('You have selected a folder to move content.');
            $uibModalInstance.close($scope.currentFolderId);
        }
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss('cancel');
    }

    onLoad();
 }]);

plApp.controller('contentInDetailMdlCtrl',['$scope','file','$uibModalInstance',
 function($scope, file, $uibModalInstance){

    var onLoad = function(){
        $scope.file = file;
    };

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
            ,start : function(event, ui){
            }
            ,stop : function(event,ui){
            }
            ,appendTo:'body'
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
              ,hoverClass : 'highlight-acceptable'
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

//content movement into folders
//maintains same scope.
plApp.directive('contentDroppable',['ctDataAccessFactory', function(ctDAF){
    return{
        restrict : 'A'
        ,link : function($scope, element,attrs){

            var postMomentFunction = function(returnData){
                if(returnData.success){
                    toastr.success('content Moved successfully');
                    $scope.refreshContent($scope.currentFolderId);
                }
                else{
                    toastr.warning(returnData.error);
                }
            };

            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : 'highlight-acceptable'
              ,drop: function(event, ui){
                   var dragIndex = angular.element(ui.draggable).data('index');
                   var draggedisFolder = angular.element(ui.draggable).data('isfolder');
                   var dropIndex = attrs['index'];
                   if(draggedisFolder){
                        if(dragIndex != dropIndex){
                            ctDAF.moveContent([$scope.folders[dragIndex].content_id],
                            $scope.folders[dropIndex].content_id, postMomentFunction);
                        }
                        else{
                            toastr.warning('You cant move the folder into the same folder');
                        }
                   }
                   else
                   {
                        ctDAF.moveContent([$scope.files[dragIndex].content_id],
                         $scope.folders[dropIndex].content_id, postMomentFunction);
                   }
                }
            });
        }
    }
}]);

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