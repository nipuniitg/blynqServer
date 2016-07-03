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
        }

        return{
            defaultSchedulesLayoutType : defaultSchedulesLayoutType
            ,layouts : layouts
        }
    }]);

}());