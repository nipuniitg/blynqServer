(function(){
'use strict';

    angular.module('mainApp').factory('blueprints', ['$q', function($q){
        function Schedule() {
            this.schedule_id = -1,
            this.schedule_title = '',
            this.schedule_screens = [],
            this.schedule_groups = [],
            this.is_split = false,
            this.selected_layout = {},
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
        function Pane(screen_pane){
            this.schedule_pane_id = -1;
            this.screen_pane = angular.copy(screen_pane);
            this.schedule_playlists = [];
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


        function ScreenLayout(){
            this.split_screen_id = -1;
            this.title = "New layout";
            this.screen_type = {};
            this.panes=[];
        }

        function LayoutPane(number){
            var numberAvailable = (typeof number !== "undefined");
            this.pane_id = -1;
            this.title = numberAvailable ? "Pane" + number : "Pane"
            this.margin_left = 0;    //in percentage
            this.margin_top = 0;    //in percentage
            this.height = 20;       //in percentage
            this.width = 25;        // in percentage
            this.z_index = numberAvailable ? number : 0;
        }


        return{
            Schedule : Schedule
            ,Pane : Pane
            ,screenBlueprint : screenBlueprint
            ,groupBlueprint : groupBlueprint
            ,playlistBlueprint : playlistBlueprint
            ,playlistItemBlueprint : playlistItemBlueprint
            ,PlaylistItem : PlaylistItem
            ,ScreenLayout : ScreenLayout
            ,LayoutPane : LayoutPane
        }
    }]);
}());