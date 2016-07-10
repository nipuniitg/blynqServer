(function(){
'use strict';

    angular.module('mainApp').factory('blueprints', ['$q', function($q){
        var scheduleBlueprint = {
            schedule_id : -1,
            schedule_title : '',
            schedule_screens : [],
            schedule_groups : [],
            schedule_playlists:[],
            timeline:{
                is_always   : !0
                ,start_date  : null
                ,end_recurring_period :null
                ,all_day     :!0
                ,start_time  :null
                ,end_time    :null
                ,frequency  :null
                ,interval   :null
                ,recurrence_absolute:null
                ,byweekno   :null
                ,byweekday  :null
                ,bymonthday :null
            }
        };
        var screenBlueprint = {
            screen_id : -1
            ,screen_name : ''
            ,address : ''
            ,aspect_ratio : ''
            ,screen_size : ''
            ,activation_key : ''
            ,resolution :''
            ,city : {
            }
        ,groups : []
    };
        var groupBlueprint = {
            group_id : -1,
            group_name : "",
            description : "",
            screens : []
        };
        var playlistBlueprint = {
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

        function PlaylistItem(contentFile, videoDurationFn){
            this.is_folder = false;
            this.title = contentFile.title;
            this.url = contentFile.url;
            this.content_type = contentFile.content_type;
            this.content_id = contentFile.content_id;

            this.playlist_item_id = -1;

            this.setDuration = function(contentFile){
                var deferred = $q.defer();
                switch (this.content_type.split("/")[1]){
                    case 'video':
                        videoDurationFn(contentFile, function(duration){
                            deferred.resolve(duration)
                        });
                        return deferred.promise
                        break;
                    default :
                        var duration = 15;
                        deferred.resolve(duration);
                        return deferred.promise
                }
            }
        }


        return{
            scheduleBlueprint : scheduleBlueprint
            ,screenBlueprint : screenBlueprint
            ,groupBlueprint : groupBlueprint
            ,playlistBlueprint : playlistBlueprint
            ,playlistItemBlueprint : playlistItemBlueprint
            ,PlaylistItem : PlaylistItem
        }
    }]);
}());