var plApp = angular.module("plApp",['as.sortable']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

plApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

plApp.factory('dataAccessFactory',['$http','$window', function($http,$window){

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

    var savePlaylist = function(playlistObj, callback)
    {
        $http({
             method : "POST",
             url : 'getPlaylistsJson',
             data : {
                playlistObj : playlistObj
             }
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });

    };

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

    return{
        getPlaylists : getPlaylists
        ,savePlaylist : savePlaylist
        ,upsertPlaylist : upsertPlaylist
        ,deletePlaylist : deletePlaylist

    };

}]);

plApp.factory('plFactory',['dataAccessFactory', function(dataAccessFactory)
{
    var playlistBluePrint = {
        playlist_id: -1,
        playlist_title: "",
        playlist_items: []
    };

    var mdlType = {
        'Add' : 0,
        'Edit' : 1
    }

    var getPlaylists = function(callback){
        dataAccessFactory.getPlaylistsJson(callback);
    };

return{
    mdlType : mdlType
    ,playlistBluePrint : playlistBluePrint
}

}]);

plApp.controller('plCtrl', ['plFactory','$scope','$window','dataAccessFactory', function(plFactory, $scope, $window, dataAccessFactory){

    var onLoad = function(){
        //playlist
        $scope.playlists =null;
        $scope.activePlaylistIndex = 0;
        $scope.activePlaylistObj = null;

        //playlist queue
        $scope.activeQueueItemIndex= null;
        $scope.activeQueueItem = null;
        $scope.dragControlListeners = {
            //accept: function (sourceItemHandleScope, destSortableScope) {return boolean}//override to determine drag is allowed or not. default is true.
            itemMoved: function (event) {},
            orderChanged: function(event) {},
            containment: '#div-playlistQueue',//optional param.
            clone: true, //optional param for clone feature.
            allowDuplicates: false //optional param allows duplicates to be dropped.
        };

        //bool values
        $scope.playlistQueueEditMode = false;
        $scope.showQueueItemDetails = false;

        $scope.displayContentDiv = false;

        getPlaylists();
    }



    //private methods
    var  getPlaylists = function(){
        dataAccessFactory.getPlaylists(function(data){
            $scope.playlists = data;
            updateActivePlaylist(0);
        });
    }

    var updateActivePlaylist = function(index){
        $scope.activePlaylistObj = angular.copy($scope.playlists[index]);
        $scope.activePlaylistIndex = index;
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
                    toastr.success('Playlist added successfully');
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
                $scope.activePlaylistIndex = null; //should be modified
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
    };


    //----edit/remove playlistItems details (title)
    $scope.editPlaylistItems = function(){
        //need selector here
        $scope.playlistQueueEditMode= true;
    };

    $scope.savePlaylistQueueItems = function(){
        dataAccessFactory.savePlaylistItems($scope.activePlaylistObj, function(data){
            if(data.success)
            {
                toastr.success('Playlist saved successfully');
                $scope.playlistQueueEditMode = false;
                playlists[$scope.activePlaylistIndex] = data.playlist;
            }
            else{
                toastr.warning('Oops!! Some error occured. Please try again.');
            }
        });
    };

    $scope.cancelPlaylistQueueItemsEdit = function(){
        $scope.playlistQueueEditMode = false;
        updateActivePlaylist($scope.activePlaylistIndex);
    }



    //Related to queue item details methods
    $scope.clickedOnQueueItem = function(index){
        $scope.showQueueItemDetails = true;
        $scope.activeQueueItem = $scope.activePlaylistObj.queueItems[index];
        $scope.activeQueueItemIndex = index;
    };

    $scope.reomveQueueItem = function(index){
        $scope.activePlaylistObj.queueItems.splice(index,1);
        if($scope.activeQueueItemIndex == index)
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