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

plApp.factory('plFactory',['plDataAccessFactory','blueprints', function(dataAccessFactory,blueprints)
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
            var folderFiles = [];
            if(noOfContents>0)
            {
                for(var i=0;i<noOfContents; i++)
                {
                    var playlistItem = new blueprints.PlaylistItem(contentItems[i]);
                    folderFiles.push(playlistItem);
                }
            }
            callback(folderFiles);
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
        $scope.contentDetailsForm={};

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
                toastr.warning(data.errors.join());
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
                                toastr.warning(returnData.errors.join());
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
        enableSortable();
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
                toastr.warning(data.errors.join());
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
    $scope.addContentToPlaylistItems = function(index, fileType){
        if(!$scope.playlistQueueEditMode)
        {
            $scope.editPlaylistItems();
            toastr.success('Playlist in edit mode.Dont forget to save after updating.');
        }
        if(fileType == 'file'){
            var contentDropped = ctFactory.getFilesObj()[index];
        }else{
            var contentDropped = ctFactory.getWidgetsObj()[index];
        }

        var newPlaylistItem = new blueprints.PlaylistItem(contentDropped);
        $scope.$apply(function(){
            $scope.activePlaylistObj.playlist_items.push(newPlaylistItem);
        });
        toastr.success('File added to playlist');
    }

    $scope.addFolderContentToPlaylistItems= function(index)
    {
        if(!$scope.playlistQueueEditMode)
        {
            $scope.editPlaylistItems();
            toastr.success('Playlist in edit mode.Dont forget to save after updating.');
        }
        toastr.success('Folder Dragged. Loading the content in the folder.');
        var folderDropped = ctFactory.getFoldersObj()[index];
        plFactory.getFolderContentsAsPlaylistItems(folderDropped.content_id, function(data){
            $scope.activePlaylistObj.playlist_items= $scope.activePlaylistObj.playlist_items.concat(data);
            toastr.success('Playlist Items updated')
        });
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
        if($scope.contentDetailsForm.form.$valid)
        {
           $scope.activePlaylistObj.playlist_items[$scope.activePlaylistItemIndex] = angular.copy($scope.activePlaylistItem);
            toastr.success('duration updated!! Dont forget to save playlist after edit.')
        }else{
            toastr.warning('Some errors are there in the input fields. Resolve them and try again');
        }

    };



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

plApp.filter('youtube', ['youtubeFactory', function(yF){
    /*
        This filter extracts the required video Id and playlist Id
        and builds a custom Url which is upported to play
     */
    return function(url){
        var controls = '?controls=1';
        var autoplay = '&autoplay=1';
        var loop = '&loop=1';
        var playlistUrlStr = '?listType=playlist&list=';
        var addAdditionalParamsToUrl = function(){
            customUrl = customUrl + controls + autoplay + loop;
        };

        var customUrl = 'https://www.youtube.com/embed/';

        //if video Id exists, then construct url with video Id, otherwise with playlistId
        if(yF.getVideoId(url)){
            customUrl = customUrl + yF.getVideoId(url);
            addAdditionalParamsToUrl();
            return customUrl
        }else{
            customUrl = customUrl +  playlistUrlStr + yf.getPlaylistId(url);
            return customUrl
        }
    }
}]);

plApp.factory('youtubeFactory', [function(){

    //returns the video Id of an Url
    var getVideoId = function(url){
        var regex = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/;
        return url.match(regex)[7]
    };

    var getPlaylistId = function(url){
        var regExp = /^.*(youtu.be\/|list=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2]){
        return match[2];
        }
    };

    return{
        getVideoId : getVideoId
        ,getPlaylistId : getPlaylistId
    };
}]);

plApp.directive('mediaPlayer', ['$timeout', function($timeout){
    return{
        restrict:'E'
        ,templateUrl : '/static/templates/shared/_media_player_drtv.html'
        ,scope:{
            mediaFile : '='
            ,muteAudio : '='
        }
        ,link : function($scope, elem, attr){

            var onLoad = function(){
                if(!('muteAudio' in attr)){
                    $scope.muteAudio = false;
                }
                $scope.showImageBlur = ('schedulePreviewMode' in attr) ? true : false;
            }

            $scope.$watch('mediaFile', function(){
                setMediaType();
            });

            $scope.isMediaType = {
                image : false
                ,video : false
                ,audio : false
                ,pdf : false
                ,youtube : false
                ,rssText : false
                ,iframe : false
                ,default : false
            };

            var setMediaType = function(){
                /*
                    sets what mime type the current playing item is. If it can't find any, it defaults to
                    default image.
                */
                angular.forEach($scope.isMediaType, function(value, key){
                    $scope.isMediaType[key] = false;
                });
                switch(true){
                    case $scope.mediaFile.content_type.indexOf('image')>-1:
                        $scope.isMediaType.image = true;
                        break;
                    case $scope.mediaFile.content_type.indexOf('pdf')>-1:
                        $scope.isMediaType.pdf = true;
                        break;
                    case $scope.mediaFile.content_type.indexOf('video')>-1:
                        $scope.isMediaType.video = true;
                        break;
                    case $scope.mediaFile.content_type.indexOf('audio')>-1:
                        $scope.isMediaType.audio = true;
                        break;
                    case $scope.mediaFile.content_type.indexOf('youtube')>-1:
                        $scope.isMediaType.youtube = true;
                        break;
                    case $scope.mediaFile.content_type.indexOf('widget/rss/text')>-1:
                        $scope.isMediaType.rssText = true;
                        setUpRssTextMedia();
                        break;
                    case $scope.mediaFile.content_type.indexOf('url/web')>-1:
                        $scope.isMediaType.iframe = true;
                        break;
                    default:
                        $scope.isMediaType.default = true;
                }
            };

            var setUpRssTextMedia = function(){
                //set font-size according to the div height
                $timeout(function(){
                    var $div = $('.media-player .rss-text');
                    var divHeight = $div.height();
                    $div.css({
                        'font-size': (divHeight/2) + 'px',
                        'line-height': divHeight + 'px'
                    });
                }, 300);
			    
            };

            onLoad();
        }
    }
}]);

