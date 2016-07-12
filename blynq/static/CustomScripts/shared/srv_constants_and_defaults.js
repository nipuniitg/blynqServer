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
            };
            return fileIcons
        }

        return{
            defaultSchedulesLayoutType : defaultSchedulesLayoutType
            ,layouts : layouts
            ,getPopOverMessages : getPopOverMessages
            ,getFileIcons : getFileIcons
        }
    }]);

}());