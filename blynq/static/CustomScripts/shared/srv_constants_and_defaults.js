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
                ,draggable : 'draggable'
                ,listView : 'List View'
                ,calendarView : 'Calendar View'
            }
            return popOverMessages
        }

        var getFileIcons = function(){
            var fileIcons = {
                pdf : '/static/images/pdf_logo.png'
                ,video : '/static/images/video_icon.png'
                ,folder : '/static/images/folder-icon.png'
                ,url : '/static/images/url_icon.png'
                ,audio : '/static/images/audio_icon.png'
            };
            return fileIcons
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

        return{
            defaultSchedulesLayoutType : defaultSchedulesLayoutType
            ,layouts : layouts
            ,getPopOverMessages : getPopOverMessages
            ,getFileIcons : getFileIcons
            ,getPaneDefaults : getPaneDefaults
            ,getAllFilesHomeFolder : getAllFilesHomeFolder
        }
    }]);

}());