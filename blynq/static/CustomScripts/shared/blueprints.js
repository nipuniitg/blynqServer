(function(){
'use strict';

    angular.module('mainApp').factory('blueprints', ['$q', function($q){
        function Schedule() {
            this.schedule_id = -1,
            this.schedule_title = '',
            this.schedule_description = '',
            this.schedule_screens = [],
            this.schedule_groups = [],
            this.layout = {},
            this.schedule_panes =[];
        };

        function SchedulePane(layout_pane){
            this.schedule_pane_id = -1;
            this.layout_pane = angular.copy(layout_pane);
            this.schedule_playlists = [];
            this.mute_audio = false;
            this.timeline ={
                is_always   : !0
                ,start_date  : null
                ,end_date    : null
                ,all_day     :!0
                ,start_time  :null
                ,end_time    :null
                ,is_repeat   : !1
                ,end_recurring_period :null
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
            ,city : {}
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
            this.thumbnail = contentFile.thumbnail;
            this.content_type = contentFile.content_type;
            this.content_id = contentFile.content_id;
            this.playlist_item_id = -1;
            this.display_time = contentFile.duration;
        }

        //layouts
        function Layout(){
            this.layout_id = -1;
            this.title = "New layout";
            this.aspect_ratio = {};
            this.layout_panes=[];
        }

        function LayoutPane(argObj){
            var numberAvailable = (typeof argObj.newPaneIndex !== "undefined");
            this.layout_pane_id = argObj.layout_pane_id ? argObj.layout_pane_id :  -1;
            this.title = argObj.title ? argObj.title :  numberAvailable ? "Pane" + argObj.newPaneIndex : "Pane"
            this.left_margin = argObj.left_margin ? argObj.left_margin : 0;    //in percentage
            this.top_margin = argObj.top_margin ? argObj.top_margin : 0;    //in percentage
            this.height = argObj.height ? argObj.height : 20;       //in percentage
            this.width = argObj.width ? argObj.width : 25;        // in percentage
            this.z_index = argObj.z_index ? argObj.z_index : numberAvailable ? argObj.newPaneIndex : 0;
            this.aspect_ratio={};

            this.calculatePaneAspectRatio = function(){
                var gcd ;
                if(argObj.layoutAspectRatio.orientation == 'LANDSCAPE'){
                    gcd = this.getGCD(this.width*argObj.layoutAspectRatio.width_component, this.height*argObj.layoutAspectRatio.height_component);
                    this.aspect_ratio.width = (this.width * argObj.layoutAspectRatio.width_component)/gcd;
                    this.aspect_ratio.height = (this.height * argObj.layoutAspectRatio.height_component)/gcd;
                }else{
                    gcd = this.getGCD(this.width*argObj.layoutAspectRatio.height_component, this.height*argObj.layoutAspectRatio.width_component);
                    this.aspect_ratio.width = (this.width * argObj.layoutAspectRatio.height_component)/gcd;
                    this.aspect_ratio.height = (this.height * argObj.layoutAspectRatio.width_component)/gcd;
                }
            };

            this.getGCD = function(a,b){
                if(b == 0)
                    return a
                return this.getGCD(b, a%b)
            }

            this.calculatePaneAspectRatio();
        };


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