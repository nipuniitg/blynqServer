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
    var deleteContent = function(contentId, callback){
        $http({
             method : "GET"
             ,url : '/content/deleteContent'+ contentId
             /*,data:{
                itemId : itemId
             }*/
         }).then(function mySuccess(response){
                if(response.data.actionStatus =="success")
                {
                    if(callback)
                    {callback();}

                }
                else
                {
                    toastr.warning("Oops!!There was some network error. Please try later.");
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

    var uploadContent = function(file, newContentObj, callback){
        var fd = new FormData();
        fd.append('file', file);
        fd.append('title', newContentObj.title);
        /*$http({
            method : "POST"
            ,url : "uploadContent"
            ,data : fd
            ,headers: {'Content-Type': undefined}
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });*/
        uploadUrl ='uploadContent'
        $http.post(uploadUrl, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
            alert('upload success');
        })
        .error(function(){
            alert('upload failed');
        });
    }

    return{
        getContentJson : getContentJson
        ,deleteContent : deleteContent
        ,getFiles : getFilesJson
        ,getFolders : getFoldersJson
        ,uploadContent : uploadContent
    }

}]);

//Any logic that needs some computation goes here.
plApp.factory('ctFactory', ['ctDataAccessFactory', function(ctDataAccessFactory){

    var getContent = function(callback)
    {
        ctDataAccessFactory.getContentJson(callback);
    };

    return{
        getContent : getContent
    }

}]);

plApp.controller('ctCtrl',['$scope','ctFactory','ctDataAccessFactory', function($scope, ctFactory, ctDataAccessFactory){

   /* $scope.dragControlListeners = {
        //accept: function (sourceItemHandleScope, destSortableScope) {return boolean}//override to determine drag is allowed or not. default is true.
        itemMoved: function (event) {},
        orderChanged: function(event) {},
        containment: '#div-playlistQueue',//optional param.
        clone: true, //optional param for clone feature.
        allowDuplicates: false //optional param allows duplicates to be dropped.
    };*/

    //private functions
    var onLoad = function(){
        $scope.currentFolderId = -1  //-1 represents root folder. And hence fetches the data in root folder.
        refreshContent($scope.currentFolderId);
    };

    var refreshContent = function(folderId){

        ctDataAccessFactory.getFolders(folderId, function(data)
        {
            $scope.folders = data;
        });

        ctDataAccessFactory.getFiles(folderId, function(data)
        {
            $scope.files = data;
        });

        $scope.currentFolderId = folderId;
    };

    //public or Scope releated functions
    $scope.deleteContent = function(content){
        ctDataAccessFactory.deleteContent(content.content_id,  function(data){
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
        ctDataAccessFactory.uploadContent(file, $scope.mdlNewFileDetailsObj, function(data){
            if(data.success){
                refreshContent($scope.currentFolderId);
                toastr.success('Upload successful');
            }
            else{
                toastr.warning('Upload failed. Please try after some time.');
            }
        });
    }

    $scope.navigateToFolder = function(contentId){
        refreshContent(contentId);
    }

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

plApp.directive('droppable', function($compile){
return{
    restrict : 'A'
    ,scope : {
        queueItems : '=data-ng-model'
    }
    ,link: function(scope, element, attrs) {
            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : '.highlight-acceptable'
              ,drop: function(event, ui){
                   var dragIndex = angular.element(ui.draggable).data('index');
                   console.log();
                   console.log();
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