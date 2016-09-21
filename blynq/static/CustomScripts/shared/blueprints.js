(function(){
'use strict';

    angular.module('mainApp').factory('blueprints', ['$q', function($q){
        function Schedule() {
            this.schedule_id = -1,
            this.schedule_title = '',
            this.schedule_screens = [],
            this.schedule_groups = [],
            this.is_split = false,
            this.layout = {},
            this.schedule_panes =[];
        };
        //            schedule_playlists:[],
//            timeline:{
//                is_always   : !0
//                ,start_date  : null
//                ,end_recurring_period :null
//                ,all_day     :!0
//                ,start_time  :null
//                ,end_time    :null
//                ,frequency  :null
//                ,interval   :null
//                ,recurrence_absolute:null
//                ,byweekno   :null
//                ,byweekday  :null
//                ,bymonthday :null
//            }

        //Todo : Below naming is inappropriate, as it is not pane but schedule Pane
        function SchedulePane(layout_pane){
            this.schedule_pane_id = -1;
            this.layout_pane = angular.copy(layout_pane);
            this.schedule_playlists = [];
            this.schedule_widgets=[];
            this.schedule_blynq_playlists=[];
            this.mute_audio = false;
            this.timeline ={
                is_always   : !0
                ,start_date  : null
                ,end_recurring_period :null
                ,all_day     :!0
                ,start_time  :null
                ,end_time    :null
                ,frequency  :"DAILY"
                ,interval   :null
                ,recurrence_absolute:null
                ,byweekno   :null
                ,byweekday  :null
                ,bymonthday :null
            };
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

        function PlaylistItem(contentFile){
            this.is_folder = false;
            this.title = contentFile.title;
            this.url = contentFile.url;
            this.content_type = contentFile.content_type;
            this.content_id = contentFile.content_id;
            this.playlist_item_id = -1;
            this.display_time = contentFile.duration;
//            this.setDuration = function(contentFile){
//                var deferred = $q.defer();
//                switch (this.content_type.split("/")[1]){
//                    case 'video':
//                        getDurationFn(contentFile, function(duration){
//                            deferred.resolve(duration)
//                        });
//                        return deferred.promise
//                        break;
//                    case 'audio':
//                        getDurationFn(contentFile, function(duration){
//                            deferred.resolve(duration)
//                        });
//                        return deferred.promise
//                        break;
//                    case 'web' :
//                        var duration = 150;
//                        deferred.resolve(duration);
//                        return deferred.promise
//                        break;
//                    default :
//                        var duration = 15;
//                        deferred.resolve(duration);
//                        return deferred.promise
//                }
//            }
        }

        //layouts
        function Layout(){
            this.layout_id = -1;
            this.title = "New layout";
            this.aspect_ratio = {};
            this.layout_panes=[];
        }

        function LayoutPane(number){
            var numberAvailable = (typeof number !== "undefined");
            this.layout_pane_id = -1;
            this.title = numberAvailable ? "Pane" + number : "Pane"
            this.left_margin = 0;    //in percentage
            this.top_margin = 0;    //in percentage
            this.height = 20;       //in percentage
            this.width = 25;        // in percentage
            this.z_index = numberAvailable ? number : 0;
        }


        return{
            Schedule : Schedule
            ,SchedulePane : SchedulePane
            ,screenBlueprint : screenBlueprint
            ,groupBlueprint : groupBlueprint
            ,playlistBlueprint : playlistBlueprint
            ,playlistItemBlueprint : playlistItemBlueprint
            ,PlaylistItem : PlaylistItem
            ,Layout : Layout
            ,LayoutPane : LayoutPane
        }
    }]);
}());