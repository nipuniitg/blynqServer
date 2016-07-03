(function(){
'use strict';

    angular.module('mainApp').factory('blueprints', [function(){
        var scheduleBlueprint = {
            schedule_id : -1,
            schedule_title : '',
            schedule_screens : [],
            schedule_groups : [],
            splitScreen : false,
            selectedLayout : {label : 'Full Screen', id: -4, panes : 1},
            panes :[]
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
        var paneBlueprint = {
            playlists : [],
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

        return{
            scheduleBlueprint : scheduleBlueprint
            ,paneBlueprint : paneBlueprint
            ,screenBlueprint : screenBlueprint
            ,groupBlueprint : groupBlueprint
            ,playlistBlueprint : playlistBlueprint
            ,playlistItemBlueprint : playlistItemBlueprint
        }
    }]);
}());