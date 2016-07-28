var plApp = angular.module("plApp",['as.sortable','ngCookies','ngPDFViewer']).config(function($interpolateProvider) {
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
             url : '/api/playlist/getPlaylists'
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
             ,url : '/api/playlist/upsertPlaylist'
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
             ,url : '/api/playlist/deletePlaylist'
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
             ,url : '/api/playlist/savePlaylistItems'
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
             ,url : '/api/playlist/getFilesRecursively/'+folderId
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

plApp.controller('plCtrl', ['plFactory','ctFactory','$scope','$window','plDataAccessFactory',
'$uibModal','blueprints','$q',
 function(plFactory,ctFactory, $scope, $window, dataAccessFactory,$uibModal,blueprints, $q){

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

    var newPlaylistIndex = -1;

    $scope.addPlaylist = function(){
        openPlaylistTitleMdl(newPlaylistIndex);
    }

    $scope.editPlaylist = function(index){
        openPlaylistTitleMdl(index);
    }

    var openPlaylistTitleMdl = function(index){
        var isNewPlaylist = index == newPlaylistIndex ? !0 : !1;

        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/playlistManagement/_playlist_title_mdl.html'
              ,controller: function($scope, $uibModalInstance, playlistObj, plDataAccessFactory){
                    var isNewPlaylist = playlistObj.playlist_id == -1 ? !0 : !1;
                    var onLoad = function(){
                        $scope.playlist = playlistObj;
                        $scope.mdlVerbose = isNewPlaylist ? 'Add' : 'Update'
                    };

                    onLoad();

                    $scope.upsertPlaylist = function(){
                        console.log($scope.playlist)
                        plDataAccessFactory.upsertPlaylist($scope.playlist, function(returnData){
                            if(returnData.success){
                                if(isNewPlaylist){
                                    toastr.success('Playlist added successfully');
                                }
                                else{
                                    toastr.success('Playlist updated successfully.')
                                }
                                $uibModalInstance.close(returnData.playlist);
                            }
                            else{
                                toastr.warning('Oops! There was some error while updating the details. Please try again later.')
                            }
                        });
                    };

                    $scope.cancel = function(){
                        $uibModalInstance.dismiss();
                    }
              }
              ,size: 'md'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve: {
                playlistObj: function(){
                    if(isNewPlaylist)
                    {
                        return angular.copy(plFactory.playlistBluePrint);
                    }
                    else{
                        return angular.copy($scope.playlists[index]);
                    }
                }
              }
        });

        modalInstance.result.then(function saved(upsertedPlaylist){
            if(isNewPlaylist){
                $scope.playlists.push(angular.copy(upsertedPlaylist));
                updateActivePlaylist($scope.playlists.length-1);
                enableSortable();
            }
            else{
                $scope.playlists[$scope.activePlaylistIndex].playlist_title = upsertedPlaylist.playlist_title;
                updateActivePlaylist($scope.activePlaylistIndex);
            }
            $scope.playlistQueueEditMode = true;
        }, function cancelled(){

        })

    }

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
                $scope.activePlaylistItem = angular.copy($scope.activePlaylistObj.playlist_items[$scope.activePlaylistItemIndex]);
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
            toastr.success('Dropped. Adding in progress..')
            var contentDropped = ctFactory.getFilesObj()[index];
            //:TODO If the dropped content is video, duration time should be set as per that video duration
            var newPlaylistItem = new blueprints.PlaylistItem(contentDropped, getVideoDuration);
            newPlaylistItem.setDuration(contentDropped).then(function(duration){
                if(duration == NaN)
                {
                    newPlaylistItem.display_time = 500;
                }else
                {
                    newPlaylistItem.display_time = duration;
                }

                    $scope.activePlaylistObj.playlist_items.push(newPlaylistItem);
                    toastr.success('File added to playlist');
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
        $scope.activePlaylistItem = angular.copy($scope.activePlaylistObj.playlist_items[index]);
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
        if($scope.contentDetailsForm.$valid)
        {
           $scope.activePlaylistObj.playlist_items[$scope.activePlaylistItemIndex] = angular.copy($scope.activePlaylistItem);
            toastr.success('duration updated!! Dont forget to save playlist after edit.')
        }else{
            toastr.warning('Some errors are there in the input fields. Resolve then and try again');
        }

    };

    //video drag drop duration
    var getVideoDuration = function(contentFile, callback){
        var duration;
        var video = document.getElementById("video_for_duration");
        //if same item dropped, then take duration from the existing
        if(video.src == contentFile.url){
            duration =  Math.ceil(video.duration);
            callback(duration);
        }
        else{
            $scope.$apply(function(){
                $scope.file = contentFile;
            });
            video.onloadedmetadata = function(){
                duration = Math.ceil(video.duration);
                callback(duration);
            };
        }
    }


    onLoad();

}]);

plApp.filter('playlistTotalTime', [function(){
    return function(playlist){
        var totalSec = 0;
        for(i=0;i<playlist.playlist_items.length;i++){
            totalSec += playlist.playlist_items[i].display_time;
        }

        var hours   = Math.floor(totalSec / 3600);
        var minutes = Math.floor((totalSec - (hours * 3600)) / 60);
        var seconds = totalSec - (hours * 3600) - (minutes * 60);

        var result = (hours < 10 ? "0" + hours : hours) + "-" + (minutes < 10 ? "0" + minutes : minutes) + "-" + (seconds  < 10 ? "0" + seconds : seconds);

        return result
    }

}]);

