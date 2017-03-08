(function(){
'use strict';

    angular.module('mainApp').factory('constantsAndDefaults', [function(){
        var defaultSchedulesLayoutType = function(){
            return 'list'
        };

        var layouts = function(){
            return layouts = [

                {label : 'Two Split(Vertical)', id : -3, panes : 2}
                ,{label : 'Two Split(Horizontal)', id : -2, panes : 2}
                ,{label : 'Three Split', id : -1, panes : 3}
            ];
        };

        var getPopOverMessages = function(){
            var popOverMessages = {
                uploadFile : 'Upload Images /videos /gifs /pdfs'
                ,addURL : 'Add youtube video links/Website urls'
                ,addWidget: 'Add RSS feed/ live event updates like weather etc'
                ,draggable : 'draggable'
                ,listView : 'List View'
                ,calendarView : 'Calendar View'
            }
            return popOverMessages
        }

        //screen layout design

        var getPaneDefaults  = function(){
            /* below values restricts the user to not to go below the mentioned measurements*/
            var paneDefaults = {
                minWidth : 5        //in percentage
                ,minHeight : 5      // in percentage
            }
            return paneDefaults
        }

        //content - all files recursive home folder : -1

        var getAllFilesHomeFolder = function(){
            return -1
        }


        var getRefreshScreensInterval = function(){
            var screensRefreshInterval = 20000;
            return screensRefreshInterval
        }

        var getPlaylistTypes = function(){
            var playlistTypes = {
                userCreatedPlaylist : 'user_created'
                ,blynqTVPlaylist  : 'blynq_tv'
                ,contentPlaylist : 'content'
                ,widgetPlaylist : 'widget'
            }
            return angular.copy(playlistTypes);
        }

        var getWidgetTypes = function(){
            var widgetTypes = {
                rss : 'rss'
                ,hdmiIn : 'hdmiIn'
                ,fb : 'fb'
                ,clock : 'clock'
                ,instagram : 'instagram'
            }
            return angular.copy(widgetTypes);
        };

        return{
            defaultSchedulesLayoutType : defaultSchedulesLayoutType
            ,layouts : layouts
            ,getPopOverMessages : getPopOverMessages
            ,getPaneDefaults : getPaneDefaults
            ,getAllFilesHomeFolder : getAllFilesHomeFolder
            ,getRefreshScreensInterval : getRefreshScreensInterval
            ,getPlaylistTypes : getPlaylistTypes
            ,getWidgetTypes : getWidgetTypes
        }
    }]);

}());