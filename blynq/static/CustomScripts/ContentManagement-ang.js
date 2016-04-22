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
    var deleteItem = function(itemId, callback){
        $http({
             method : "GET"
             ,url : '/content/deleteItem'
             /*,data:{
                itemId : itemId
             }*/
         }).then(function mySuccess(response){
                if(response.data.actionStatus =="success")
                {
                    if(callback)
                    {callback();}
                    toastr.success('Item deleted successfully.');
                }
                else
                {
                    toastr.warning("Oops!!There was some network error. Please try later.");
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var deleteFolder = function(folderId, callback){
        $http({
             method : "POST"
             ,url : '/content/deleteFolder'
             /*,data:{
                folderId : folderId
             }*/
         }).then(function mySuccess(response){
                if(response.data.actionStatus =="success")
                {
                    if(callback)
                    {callback();}
                    toastr.success('Folder deleted successfully.');
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


    return{
        getContentJson : getContentJson,
        deleteItem : deleteItem,
        deleteFolder : deleteFolder,
        getFiles : getFilesJson,
        getFolders : getFoldersJson
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
        /*ctFactory.getContent(function(data){
            $scope.contentObj = data;
        });*/

        ctDataAccessFactory.getFolders(folderId, function(data)
        {
            $scope.folders = data;
        });

        ctDataAccessFactory.getFiles(folderId, function(data)
        {
            $scope.files = data;
        });
    };

    //public or Scope releated functions
    $scope.deleteItem = function(index){
        ctDataAccessFactory.deleteItem($scope.contentObj.items[index].itemId,  function(){
            $scope.contentObj.items.splice(index, 1);
        });
    }

    $scope.deleteFolder = function(index){
        ctDataAccessFactory.deleteFolder($scope.contentObj.folders[index].folderId,  function(){
            $scope.contentObj.folders.splice(index, 1);
        });
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
/*    ,scope : {
        queueItems : '='
    }*/
    ,link: function(scope, element, attrs) {
            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : '.highlight-acceptable'
              ,drop: function(event, ui){
                   var dragIndex = angular.element(ui.draggable).data('index');
                   console.log(scope);
                   console.log(scope.contentObj);
                }
            });

        }
}});