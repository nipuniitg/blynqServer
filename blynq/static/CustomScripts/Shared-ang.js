var shApp = angular.module("shApp", []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

shApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


shApp.factory('cookDateTime', [function(){

    var getOnlyTime = function(datetime){
        if(datetime== null){
            return null
        }
        else{
            return datetime.getHours()+':'+ datetime.getMinutes()
        }
        };

    var getOnlyDate = function(datetime){
        if(datetime == null)
        {
           return null
        }
        else{
            return (datetime.getFullYear() + '/' + (datetime.getMonth()+1)+'/'+ datetime.getDate())
        }

    }

    var getDateTimeFromDate = function(dateString){
        if(dateString==null)
        {
            return null;
        }
        else{
            var newDate = new Date(dateString);
            return newDate
        }
    }

    var getDateTimeFromTime = function(timeString){
        if(timeString == null){
            return null;
        }
        else{
            var dateTime =  new Date();
            dateTime.setHours(timeString.split(':')[0]);
            dateTime.setMinutes(timeString.split(':')[1]);
            return dateTime;
        }

    }

    return{
        getOnlyTime : getOnlyTime
        ,getOnlyDate : getOnlyDate
        ,getDateTimeFromDate : getDateTimeFromDate
        ,getDateTimeFromTime : getDateTimeFromTime
    }

}]);

shApp.filter('showOnlyDate',['cookDateTime', function(cDT){
    return function(dateTime){
        var dateOnly = cDT.getOnlyDate(dateTime)
        return dateOnly
    }
}])

shApp.filter('showOnlyTime',['cookDateTime', function(cDT){
    return function(dateTime){
        var timeOnly = cDT.getOnlyTime(dateTime)
        return timeOnly
    }
}])

shApp.filter('inHoursFormat', [function(){
    return function(totalSec){
        var hours   = Math.floor(totalSec / 3600);
        var minutes = Math.floor((totalSec - (hours * 3600)) / 60);
        var seconds = totalSec - (hours * 3600) - (minutes * 60);
        var result = (hours < 10 ? "0" + hours : hours) + "-" + (minutes < 10 ? "0" + minutes : minutes) + "-" + (seconds  < 10 ? "0" + seconds : seconds);
        return result
    }
}])