(function(){
'use strict';

    angular.module('mainApp').factory('constantsAndDefaults', [function(){
        var defaultSchedulesLayoutType = function(){
            return 'list'
        };

        return{
            defaultSchedulesLayoutType : defaultSchedulesLayoutType
        }
    }]);

}());