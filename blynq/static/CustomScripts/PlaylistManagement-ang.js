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

    var getPlaylistsJson = function(callback){
         $http({
             method : "GET",
             url : 'getPlaylistsJson'
         }).then(function mySucces(response){
                returnData = angular.copy(response.data);
                if(callback)
                {
                    callback(returnData);
                }
                return returnData
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
                return returnData
            }, function myError(response) {
                console.log(response.statusText);
            });

    };

    return{
        getPlaylistsJson : getPlaylistsJson,
        savePlaylist : savePlaylist
    };

}]);

plApp.factory('plFactory',['dataAccessFactory', function(dataAccessFactory)
{
    var playlistBluePrint = {
    playlistId: 1,
    playlistName: "dummy",
    queueItems: []};

    var getPlaylists = function(callback){
        dataAccessFactory.getPlaylistsJson(callback);
    };

return{
    getPlaylists : getPlaylists,
    playlistBluePrint : playlistBluePrint
}

}]);

plApp.controller('plCtrl', ['plFactory','$scope','$window', function(plFactory, $scope, $window){

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


    plFactory.getPlaylists(function(playlists){
        $scope.playlists = angular.copy(playlists);
        $scope.activePlaylistObj = $scope.playlists[0];
    });

    //methods
    $scope.addPlyalist = function(){
        $scope.activePlaylistObj = angular.copy(plFactory.playlistBluePrint);
    };

    $scope.saveAddPlaylist = function(){
        //ajax save activePlaylistObj(only name will be there). and add it to the playlists
        $scope.playlists.push(angular.copy($scope.activePlaylistObj));
        $scope.activePlaylistIndex = $scope.playlists.length -1;
        $scope.playlistQueueEditMode = true;
    }

    $scope.cancelAddPlaylist = function(){
        $scope.activePlaylistObj = angular.copy($scope.playlists[$scope.activePlaylistIndex]);
    };

    $scope.deletePlaylist = function(){
        //ajax delete playlsit and once confirms... remove it from playlists here.

    };

    $scope.editPlaylist = function(){
        //need selector here
        $scope.playlistQueueEditMode= true;
    };

    $scope.savePlaylistQueueItems = function(){
        $scope.playlistQueueEditMode = false;
    };

    $scope.cancelPlaylistQueueItemsEdit = function(){
        $scope.playlistQueueEditMode = false;
        $scope.activePlaylistObj = angular.copy($scope.playlists[$scope.activePlaylistIndex]);
    }

    $scope.clickedOnPlaylist= function(playlist, $index){
        $scope.activePlaylistObj = angular.copy(playlist)
        $scope.activePlaylistIndex = $index;
    };

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

}]);