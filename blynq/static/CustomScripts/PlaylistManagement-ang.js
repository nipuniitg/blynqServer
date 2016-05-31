var plApp = angular.module("plApp",['as.sortable','ui.bootstrap','ngCookies','ngPDFViewer']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

plApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

plApp.factory('plDataAccessFactory',['$http','$window', function($http,$window){

    var getPlaylists = function(callback){
         $http({
             method : "GET",
             url : 'getPlaylists'
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    //This function is used for add/edit playlist and editing playlist-items.
    var upsertPlaylist = function(playlist, callback){
        $http({
             method : "POST"
             ,url : 'upsertPlaylist'
             ,data : playlist
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var deletePlaylist = function(playlist, callback){
        $http({
             method : "POST"
             ,url : 'deletePlaylist'
             ,data : playlist
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var savePlaylistItems = function(playlist, callback)
    {
        $http({
             method : "POST"
             ,url : 'savePlaylistItems'
             ,data : playlist
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var getFolderContentsRecursively = function(folderId, callback)
    {
        $http({
             method : "GET"
             ,url : 'getFilesRecursively/'+folderId
         }).then(function mySucces(response){
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
        getPlaylists : getPlaylists
        ,upsertPlaylist : upsertPlaylist
        ,deletePlaylist : deletePlaylist
        ,getFolderContentsRecursively : getFolderContentsRecursively

    };

}]);

plApp.factory('plFactory',['plDataAccessFactory', function(dataAccessFactory)
{
    //TODO: Refactor the below code. Get the templates from the backend.
    var playlistBluePrint = {
        playlist_id: -1,
        playlist_title: "",
        playlist_items: []
    };

    var playlistItemBlueprint = {
        playlist_item_id : -1
        ,content_id: -1
        ,url: ''
        ,display_time: 15
        ,title: ''
    }

    var mdlType = {
        'Add' : 0,
        'Edit' : 1
    }

    var getFolderContentsAsPlaylistItems = function(folderId, callback){
        dataAccessFactory.getFolderContentsRecursively(folderId, function(contentItems){
            var noOfContents = contentItems.length;
            if(noOfContents>0)
            {
                for(var i=0;i<noOfContents; i++)
                {
                    contentItems[i].playlist_item_id =-1
                    contentItems[i].display_time= 15
                }
            }
            callback(contentItems);
        })

    }


return{
     mdlType : mdlType
    ,playlistBluePrint : playlistBluePrint
    ,playlistItemBlueprint : playlistItemBlueprint
    ,getFolderContentsAsPlaylistItems : getFolderContentsAsPlaylistItems
}

}]);

plApp.controller('plCtrl', ['plFactory','ctFactory','$scope','$window','plDataAccessFactory', function(plFactory,ctFactory, $scope, $window, dataAccessFactory){

    var onLoad = function(){
        //playlist
        $scope.playlists =null;
        $scope.activePlaylistIndex = 0;
        $scope.activePlaylistObj = null;

        //playlist queue
        $scope.activePlaylistItemIndex= null;
        $scope.activePlaylistItem = null;

        //bool values
        $scope.playlistQueueEditMode = false;
        $scope.showQueueItemDetails = false;

        $scope.is_sortable_disabled = !0;

        refreshPlaylists();
    };

    //private methods
    var  refreshPlaylists = function(){
        dataAccessFactory.getPlaylists(function(data){
            $scope.playlists = data;
            updateActivePlaylist(0);
        });
    }

    var updateActivePlaylist = function(index){
        $scope.activePlaylistObj = angular.copy($scope.playlists[index]);
        $scope.activePlaylistIndex = index;
        $scope.showQueueItemDetails = false;
    }

    var enableSortable = function(){
        $scope.is_sortable_disabled = !1;
    };

    var disableSortable = function(){
        $scope.is_sortable_disabled = !0;
    }



    //methods
    //----add / edit playlist (title)
    $scope.addPlaylist = function(){
        $scope.mdlPlaylist = angular.copy(plFactory.playlistBluePrint);
        $scope.mdlType = plFactory.mdlType['Add'];
    };

    $scope.editPlaylist = function(playlist, index){
        $scope.mdlPlaylist = angular.copy(playlist);
        $scope.mdlType = plFactory.mdlType['Edit'];
    }

    $scope.upsertPlaylist = function(){
        dataAccessFactory.upsertPlaylist($scope.mdlPlaylist, function(data){
            if(data.success)
            {
                if($scope.mdlType == plFactory.mdlType['Add'])
                {
                    toastr.success('Playlist added successfully. Now drag and drop content into Playlist items');
                    $scope.playlists.push(data.playlist);
                    updateActivePlaylist($scope.playlists.length-1);
                }
                else
                {
                    $scope.playlists[$scope.activePlaylistIndex].playlist_title = data.playlist.playlist_title;
                    toastr.success('Playlist name updated successfully');
                }
                $scope.playlistQueueEditMode = true;
            }
            else{
                toastr.warning('Oops!! Some error occured. Please try again.');
            }
        });


        //ajax save activePlaylistObj(only name will be there). and add it to the playlists
        //$scope.playlists.push(angular.copy($scope.activePlaylistObj));

    }

    $scope.deletePlaylist = function(index){
        dataAccessFactory.deletePlaylist($scope.playlists[index], function(data){
            if(data.success)
            {
                toastr.success('Playlist deleted successfully');
                $scope.playlists.splice(index, 1);
                updateActivePlaylist(0);
            }
            else
            {
                toastr.warning('Oops!! Some error occured. Please try again');
            }
        });
    };
    //---- add / edit plyalist


    $scope.clickedOnPlaylist= function(index){
        updateActivePlaylist(index);
        $scope.playlistQueueEditMode = false;
    };


    //----edit/remove playlistItems details (title)
    $scope.editPlaylistItems = function(){
        //need selector here
        $scope.playlistQueueEditMode= true;
        enableSortable()
        console.log($scope.activePlaylistObj);
    };

    $scope.savePlaylistQueueItems = function(){
        dataAccessFactory.upsertPlaylist($scope.activePlaylistObj, function(data){
            if(data.success)
            {
                toastr.success('Playlist saved successfully');
                $scope.playlistQueueEditMode = false;
                $scope.playlists[$scope.activePlaylistIndex] = data.playlist;
                $scope.activePlaylistObj = angular.copy($scope.playlists[$scope.activePlaylistIndex]);
                disableSortable();
            }
            else{
                toastr.warning('Oops!! Some error occured. Please try again.');
            }
        });
    };

    $scope.cancelPlaylistQueueItemsEdit = function(){
        $scope.playlistQueueEditMode = false;
        disableSortable();
        updateActivePlaylist($scope.activePlaylistIndex);
    };

    //----Add Contents To activePlaylistObj
        //Below functions are being called from the droppable directive
    $scope.addContentToPlaylistItems = function(index){
        if($scope.playlistQueueEditMode)
        {
            toastr.success('dropped')
            var contentDropped = ctFactory.getFilesObj()[index];
            var newPlaylistItem = angular.copy(plFactory.playlistItemBlueprint);
            newPlaylistItem.title = contentDropped.title;
            newPlaylistItem.url  = contentDropped.url;
            newPlaylistItem.content_id = contentDropped.content_id;
            //:TODO If the dropped content is video, duration time should be set as per that video duration

            //Had to put apply manually as the DOM is not updated by itself.
            $scope.$apply(function(){
                 $scope.activePlaylistObj.playlist_items.push(newPlaylistItem);
            });
        }
        else
        {
            toastr.warning('Please set the playlist items in edit mode.');
        }


    }

    $scope.addFolderContentToPlaylistItems= function(index)
    {
        if($scope.playlistQueueEditMode)
        {
            toastr.success('Folder Dragged. Loading the content in the folder.');
            var folderDropped = ctFactory.getFoldersObj()[index];
            plFactory.getFolderContentsAsPlaylistItems(folderDropped.content_id, function(data){
                $scope.activePlaylistObj.playlist_items= $scope.activePlaylistObj.playlist_items.concat(data);
                toastr.success('Playlist Items updated')
            });
        }
        else{
            toastr.warning('Please set the playlist items in edit mode.');
        }

    }



    //Related to queue item details methods
    $scope.clickedOnQueueItem = function(index){
        $scope.showQueueItemDetails = true;
        $scope.activePlaylistItem = $scope.activePlaylistObj.playlist_items[index];
        $scope.activePlaylistItemIndex = index;
    };

    $scope.reomveQueueItem = function(index){
        $scope.activePlaylistObj.playlist_items.splice(index,1);
        if($scope.activePlaylistItemIndex == index)
        {
            $scope.showQueueItemDetails = false;
        }
    }

    $scope.closeQueueItemDetails = function(){
        $scope.showQueueItemDetails = false;
    };

    $scope.saveItemDurationUpdate = function(){
        $scope.showQueueItemDetails = false;
    };

    onLoad();

}]);

