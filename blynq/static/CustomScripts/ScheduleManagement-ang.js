var sdApp = angular.module("sdApp",[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

sdApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
////
//schedule index material
sdApp.controller('scheduleIndexCtrl', ['$scope','scheduleIndexFactory','$uibModal',
    function($scope,sIF, $uibModal){

    var onLoad = function(){
        $scope.refreshSchedules();
    };

    $scope.refreshSchedules = function(){
        sIF.getSchedules(function(data){
            $scope.schedules = data;
        });
    };

    onLoad();

}]);

sdApp.factory('scheduleIndexFactory', ['$http', function($http){

    var getSchedules = function(callback){
        $http({
             method : "GET",
             url : '/api/schedule/getSchedules'
         }).then(function mySucces(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var deleteSchedule = function(schedule_id, callback){
      var obj = {
        schedule_id : schedule_id
      };
        $http({
            method : "POST"
            ,url : "/api/schedule/deleteSchedule"
            ,data : obj
        }).then(function mySucces(response){
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
            toastr.warning('Internal Error');
        });
    };

    return{
        getSchedules : getSchedules
        ,deleteSchedule : deleteSchedule
    }
}]);

sdApp.filter('timelineLabel', ['timelineFactory','timelineDescription', function(tF, tD) {
    return function(timeline){
        var cookedTimeline = tF.getTimeline(
            timeline.is_always
            ,tF.getDateTimeFromDate(timeline.start_date)
            ,tF.getDateTimeFromDate(timeline.end_recurring_period)
            ,timeline.all_day
            ,tF.getDateTimeFromTime(timeline.start_time)
            ,tF.getDateTimeFromTime(timeline.end_time)
            ,timeline.frequency
            ,timeline.interval
            ,timeline.recurrence_absolute
            ,timeline.bymonthday
            ,timeline.byweekno
            ,timeline.byweekday
        );
        return tD.updateLabel(cookedTimeline);
    };
}]);
//**end schedule index material

//schedules-list and schedules-calendar
sdApp.directive('schedulesList',['$log','scheduleIndexFactory','$uibModal',
    function($log, sIF, $uibModal){
    return{
        restrict    :   'E'
        ,scope      :   {
            schedules : '=schedules'
            ,refreshSchedules : '&refreshSchedulesFn'
            ,title : '@'
        }
        ,templateUrl:   '/static/templates/scheduleManagement/_schedules_list.html'
        ,link : function($scope){
                var openModalPopup = function(index){
                    var modalInstance = $uibModal.open({
                      animation: true,
                      templateUrl: '/static/templates/scheduleManagement/schedule_details.html',
                      controller: 'scheduleDetailsCtrl',
                      size: 'lg'
                      ,backdrop: 'static' //disables modal closing by click on the backdrop.
                      ,resolve: {
                        schedule: function(){
                            return angular.copy($scope.schedules[index]);
                        }
                      }
                    });

                    modalInstance.result.then(function saved(){
                        $scope.refreshSchedules();
                    }, function cancelled(){
                        toastr.warning('schedule cancelled')
                    })
                };

                $scope.editSchedule = function(index){
                    openModalPopup(index);
                };

                $scope.deleteSchedule = function(index){
                    sIF.deleteSchedule($scope.schedules[index].schedule_id, function(returnData){
                        if(returnData.success){
                            toastr.success('Deleted Schedule successfully');
                            $scope.refreshSchedules();
                        }
                        else{
                            toastr.warning('There was some error while deleting scheduling.Please refresh and try again.');
                        }
                    });
                };

                /*define searchSchedules and groups.
                Without below watch gives an error as those properties would be for undefined.*/
                $scope.searchSchedules = {};
//                $scope.searchSchedules.schedule_groups = {};
//                //to make sure search happen for both screen name and group name
                $scope.$watch('searchSchedules.schedule_screens.screen_name', function(newValue){
                    if(typeof newValue !== "undefined"){
                        $scope.searchSchedules['schedule_groups']['group_name'] = newValue;
                    }
                })
        }
    }
}]);

sdApp.directive('schedulesCalendar',['$log','scheduleIndexFactory','$uibModal',
    function($log, sIF, $uibModal){
    return{
        restrict    :   'E'
        ,scope : true
        ,bindToController : {
            rawEvents : '=events'
            ,refreshEvents : '&refreshEventsFn'
        }
        ,templateUrl: '/static/templates/scheduleManagement/_schedules_calendar.html'
        ,controller : ['$scope','calendarFactory','$uibModal', function($scope, cF, $uibModal){
                        var clndrCtrl = this;
                        var onLoad = function(){
                            clndrCtrl.calendarViewTypes = cF.calendarViewTypes;
                            clndrCtrl.calendarView = clndrCtrl.calendarViewTypes.month;
                            clndrCtrl.viewDate = moment().toDate();
                        };
                        onLoad();

                        $scope.$watch(function(){
                            return clndrCtrl.rawEvents
                        }, function(newVal){
                            clndrCtrl.events = [];
                            //This will cook the rawEvents and push the sets the variable given to calendar directive
                            if(newVal){
                                for(i=0;i<clndrCtrl.rawEvents.length;i++){
                                    var event = angular.copy(clndrCtrl.rawEvents[i]);
                                    event.startsAt = moment(event.startsAt).toDate();
                                    event.endsAt = moment(event.endsAt).toDate();
                                    clndrCtrl.events.push(event);
                                }
                            }


                        })

                        clndrCtrl.editSchedule= function(schedule){
                            var modalInstance = $uibModal.open({
                              animation: true,
                              templateUrl: '/static/templates/scheduleManagement/schedule_details.html',
                              controller: 'scheduleDetailsCtrl',
                              size: 'lg'
                              ,backdrop: 'static' //disables modal closing by click on the backdrop.
                              ,resolve: {
                                schedule: function(){
                                    return angular.copy(schedule);
                                }
                              }
                            });
                            modalInstance.result.then(function saved(){
                                clndrCtrl.refreshEvents()(clndrCtrl.viewDate.month()+1);
                            }, function cancelled(){
                                toastr.warning('schedule cancelled')
                            })
                        };

                        $scope.$watch(angular.bind(this, function () {
                          return clndrCtrl.viewDate;
                        }), function (newVal, oldVal) {
                            var oldDateMonth = moment(oldVal).month();
                            var newDateMonth = moment(newVal).month();
                            if(oldDateMonth !== newDateMonth){
                                clndrCtrl.refreshEvents()(newDateMonth+1);
                            }
                        });

                        //events
                        clndrCtrl.eventClicked = function(event) {
                          var modalInstance = $uibModal.open({
                              animation: true
                              ,templateUrl: '/static/templates/contentManagement/_content_view_mdl.html'
                              ,controller: ['$scope','$uibModalInstance','resolvedObj',
                               function($scope,$uibModalInstance,resolvedObj)
                              {
                                  var onLoad = function(){
                                    $scope.slideContent = resolvedObj.slideContent
                                    $scope.index = resolvedObj.index
                                  }

                                  onLoad();

                                  $scope.$watch('index', function(n){
                                    $scope.file = $scope.slideContent[n];
                                  });

                                  $scope.nextSlide = function(){
                                    if(($scope.index + 1)<($scope.slideContent.length)){
                                        $scope.index = $scope.index + 1;
                                    }
                                  }

                                  $scope.previousSlide = function(){
                                    if(($scope.index -1) > -1){
                                        $scope.index = $scope.index - 1;
                                    }
                                  }
                              }]
                              ,size: 'lg'
                              ,windowTemplateUrl : '/static/templates/shared/_mdl_window_template.html'
                              ,resolve : {
                                    resolvedObj : function(){
                                        var obj ={};
                                        obj.slideContent = [];
                                        for(i=0;i<event.schedule.schedule_playlists.length;i++){
                                            angular.extend(obj.slideContent, event.schedule.schedule_playlists[i].playlist_items);
                                        }
                                        if($scope.index){
                                            obj.index = angular.copy(parseInt($scope.index));
                                        }else{
                                            obj.index = 0;
                                        }

                                        return obj;
                                    }
                              }
                            });
                        };

                        clndrCtrl.eventEdited = function(event) {
                            clndrCtrl.editSchedule(event.schedule);
                        };
                    }]
        ,controllerAs : 'clndrCtrl'
    }
}]);
//**end schedules-list and schedules-calendar


//schedule Details material
sdApp.factory('scheduleDetailsFactory', ['$log','$http','$q', function($log, $http,$q){

    var selectedBoolSetter = function(allItems, selectedItems, key, schedule_key_id){
        var r = []
        ,allItemsLength = allItems.length;

        if (typeof(selectedItems) !== 'undefined'){
            selectedItemsLength = selectedItems.length;
        }
        for(i=0; i<allItemsLength; i++){
            var item = allItems[i];
            if(typeof(selectedItemsLength) !== 'undefined')
            {
                for(l=0; l<selectedItemsLength; l++){
                if(item[key] == selectedItems[l][key]){
                    //set selected bool
                    item['selected']= !0;
                    //set schedule_key_id value from the selected values
                    item[schedule_key_id] = selectedItems[l][schedule_key_id];
                    selectedItemsLength -= 1;
                    selectedItems.splice(l,1);
                    break;
                }
                }
            }
            if(!item['selected']){
                item['selected'] = !1;
                //set the new schedule_key_id(schedule_playlist_id, schedule_screen_id, schedule_group_id) as -1
                item[schedule_key_id] = -1;
            }
            r.push(item);
        }
        return r;
    };

    var getSelectedItems = function(allItems){
        var selectedItems = [];
        var allItemsLength = allItems.length;
        for(i=0; i<allItemsLength; i++){
            if(allItems[i].selected){
                delete allItems[i].selected;
                selectedItems.push(allItems[i]);
            }
        }
        return selectedItems;
    };

    var upsertScheduleDetails = function(schedule, callback){
        $http({
            method : "POST"
            ,url : "/api/schedule/upsertSchedule"
            ,data : schedule
        }).then(function mySucces(response){
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getCustomLayouts = function(){
        //This fetches all the layouts that belong to an organization
        var deferred = $q.defer();
        $http({
            method : "GET",
            url : "/api/layout/getLayouts"
        }).then(function mySucces(response){
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    };

    var getDefaultLayouts = function(){
        //This fetches default layouts --FullScreen
        var deferred = $q.defer();
        $http({
            method : "GET",
            url : "/api/layout/getDefaultLayouts"
        }).then(function mySucces(response){
            deferred.resolve(response.data);
        }, function myError(response) {
            console.log(response.statusText);
            deferred.reject(response.Text)
        });
        return deferred.promise
    };

    var getBlynqPlaylists = function(){
        var deferred = $q.defer();
        $http({
             method : "GET"
             ,url : '/api/playlist/getBlynqPlaylists'
         }).then(function mySuccess(response){
                deferred.resolve(response.data);
            }, function myError(response) {
                deferred.reject(response.text);
            });
        return deferred.promise
    };

    var getDefaultBlynqPlaylists = function(){
        //This funcation gets all blynq playlists and update them to insert into schedule.
        //So that, by default user can see Blynq content already selected in a pane.
        var deferred = $q.defer();
        getBlynqPlaylists().then(function(allBlynqPlaylists){
            for(i=0;i<allBlynqPlaylists.length;i++){
                //As blynq Playlists are also playlists 'schedule_playlist_id' remains same
                allBlynqPlaylists[i].schedule_playlist_id = -1;
            }
            deferred.resolve(allBlynqPlaylists);
        });
        return deferred.promise;
    }

    return{
        selectedBoolSetter : selectedBoolSetter
        ,getSelectedItems : getSelectedItems
        ,upsertScheduleDetails : upsertScheduleDetails
        ,getCustomLayouts : getCustomLayouts
        ,getDefaultLayouts : getDefaultLayouts
        ,getBlynqPlaylists : getBlynqPlaylists
        ,getDefaultBlynqPlaylists : getDefaultBlynqPlaylists
    }
}]);

sdApp.controller('scheduleDetailsCtrl', ['$scope','$uibModal','$log', 'scheduleDetailsFactory','constantsAndDefaults',
'$uibModalInstance','schedule','blueprints',
 function($scope, $uibModal, $log, sDF,cAD, $uibModalInstance, schedule,blueprints){

    var isNewSchedule;
    var onLoad = function(){
        $scope.schedule = schedule;
        isNewSchedule = schedule.schedule_id == -1 ? !0 : !1;
        sDF.getCustomLayouts().then(function(layouts){
            $scope.layouts =angular.copy(layouts);
        });
        sDF.getDefaultLayouts().then(function(layouts){
            $scope.fullScreenLayout = angular.copy(layouts[0]);
        });
        $scope.title = isNewSchedule? 'Add Schedule' : 'Edit Schedule';
        $scope.activeTabIndex=0;
    }
    onLoad();

    $scope.splitScreenToggled = function(){
        if(!$scope.schedule.is_split) //if not split screen, keep only one pane.
        {
            //Keep selected_layout as  Full Screen Layout
            $scope.schedule.layout = $scope.fullScreenLayout;
        }
        else //keep the default selected to one from the layouts
        {
            $scope.schedule.layout = $scope.layouts[0];
        }
    }

    /*when layout changes, the number of panes change. so remove existing panes and insert new.*/
    $scope.$watch('schedule.layout', function(newLayout,oldLayout){
        if (newLayout !== oldLayout) {
            var totalPanes = newLayout.layout_panes.length;
            $scope.schedule.schedule_panes = [];
            for(i =0; i< totalPanes; i++){
                $scope.schedule.schedule_panes.push(new blueprints.SchedulePane(newLayout.layout_panes[i]));
            }
            //For one of the panes, select blynq Content by default
            //not allowing blynq content for now.
            if(false){
                sDF.getDefaultBlynqPlaylists().then(function(allPlaylists){
                    $scope.schedule.schedule_panes[0].schedule_blynq_playlists = angular.copy(allPlaylists);
                })
            }

            $scope.activeTabIndex = 0;
        }
    });

    //Todo : Need rewrite this function according to the split screen requirement
    var validateSchedule = function(){
        if($scope.schedule.schedule_playlists.length<1)
        {
            toastr.warning('Please select atleast one playlist');
            return false
        }
        if($scope.schedule.schedule_screens.length < 1 && $scope.schedule.schedule_groups.length < 1 )
        {
            toastr.warning('Please select atleast one screen or group');
            return false
        }

        if($scope.scheduleDetailsForm.$valid)
        {
            return true;
        }
        else{
            toastr.warning('Plese fill all required fields');
        }
    };

    $scope.saveSchedule= function(){
        $log.log($scope.schedule);
        //if(validateSchedule()){
            sDF.upsertScheduleDetails($scope.schedule, function(data){
            if(data.success)
            {
                if(isNewSchedule)
                {
                    toastr.success('New Schedule Added');
                }
                else{
                    toastr.success('Schedule updated successfully');
                }
                $uibModalInstance.close($scope.schedule);
            }
            else
            {
                toastr.warning('Oops!.There was some error while updating the schedule.');
            }
        });
        //}
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss();
    };
}]);
//**end schedule details material

//timeline material
sdApp.directive('timelineTextbox', function(){
return{
    restrict: 'E'
    ,scope : {
        timeDefined :'='
        ,startDate :'='
        ,endDate :'='
        ,allDay : '='
        ,startTime :'='
        ,endTime :'='
        ,recurrenceType    :'='
        ,recurrenceFrequency  :'='
        ,recurrenceAbsolute    :'='
        ,recurrenceDayOfMonth  :'='
        ,recurrenceWeekOfMonth :'='
        ,recurrenceDaysOfWeek  :'='
    }
    ,templateUrl : '/static/templates/scheduleManagement/_timeline_textbox.html'
    ,controller : 'timelinetextboxController'
    ,link : function($scope,element, attr){

    }
}
});

sdApp.factory('timelineFactory', ['$log', function($log){

    //private methods

    var timeFunction = function(hours, minutes){
        var today = new Date();
        today.setHours(hours);
        today.setMinutes(minutes);
        return today
    };

    var e = {
        DAILY: "DAILY",
        WEEKLY: "WEEKLY",
        MONTHLY: "MONTHLY",
        YEARLY: "YEARLY"
    };

    //public methods
    var getTimeline = function(timeDefined, startDate, endDate, allDay, startTime, endTime,
                                recurrenceType,recurrenceFrequency, recurrenceAbsolute,
                                recurrenceDayOfMonth, recurrenceWeekOfMonth, recurrenceDaysOfWeek)
                                {
        var today = new Date();
        var timeline = {
            timeDefined             :   timeDefined
            ,startDate              :   startDate || today
            ,endDate                :   endDate || today
            ,allDay                 :   allDay
            ,startTime              :   startTime ||  timeFunction(0,0)
            ,endTime                :   endTime   ||  timeFunction(23,59)
            ,recurrenceType         :   recurrenceType || null
            ,recurrenceFrequency    :   recurrenceFrequency || 1
            ,recurrenceAbsolute     :   recurrenceAbsolute  || null
            ,recurrenceDayOfMonth   :   recurrenceDayOfMonth || null
            ,recurrenceWeekOfMonth  :   recurrenceWeekOfMonth|| null
            ,recurrenceDaysOfWeek   :   recurrenceDaysOfWeek || null
        };

        return timeline;

    };

    var getTimelineRecurrenceWise = function(n){
        var i = n
          , r = {
            daily: {
                recurrenceFrequency: 1
            },
            weekly: {
                recurrenceFrequency: 1
            },
            monthly: {
                recurrenceAbsolute: !1,
                absolute: {
                    recurrenceFrequency: 1,
                    recurrenceDayOfMonth: 1
                },
                relative: {
                    recurrenceFrequency: 1,
                    recurrenceWeekOfMonth: 0,
                    recurrenceDayOfWeek: 0
                }
            }
        }
          , a = function() {
            if (i.recurrenceType === e.DAILY)
            {
                r.daily.recurrenceFrequency = i.recurrenceFrequency;
            }
            else
             {
                if (i.recurrenceType === e.WEEKLY)
                {
                    r.weekly.recurrenceFrequency = i.recurrenceFrequency;
                        for (var t = 0; t < i.recurrenceDaysOfWeek.length; t++)
                            "Mon" === i.recurrenceDaysOfWeek[t] ? r.weekly.monday = !0 : "Tue" === i.recurrenceDaysOfWeek[t] ? r.weekly.tuesday = !0 : "Wed" === i.recurrenceDaysOfWeek[t] ? r.weekly.wednesday = !0 : "Thu" === i.recurrenceDaysOfWeek[t] ? r.weekly.thursday = !0 : "Fri" === i.recurrenceDaysOfWeek[t] ? r.weekly.friday = !0 : "Sat" === i.recurrenceDaysOfWeek[t] ? r.weekly.saturday = !0 : "Sun" === i.recurrenceDaysOfWeek[t] && (r.weekly.sunday = !0)
                }
                else
                {
                    //i.recurrenceType === e.MONTHLY ?
                     (r.monthly.recurrenceAbsolute = i.recurrenceAbsolute,
                        i.recurrenceAbsolute ?
                            (r.monthly.absolute.recurrenceFrequency = i.recurrenceFrequency,
                            r.monthly.absolute.recurrenceDayOfMonth = i.recurrenceDayOfMonth)
                            : (r.monthly.relative.recurrenceFrequency = i.recurrenceFrequency,
                            r.monthly.relative.recurrenceWeekOfMonth = i.recurrenceWeekOfMonth,
                            r.monthly.relative.recurrenceDayOfWeek = i.recurrenceDayOfWeek)
                     )

                }
             }
          }
          , o = function() {
            i.allDay && (i.startTime = timeFunction(8, 0),
            i.endTime = timeFunction(17, 30)),
            a()
        };
        o();
        var s = function() {
            i.recurrenceType === e.DAILY ? i.recurrenceFrequency = r.daily.recurrenceFrequency : i.recurrenceType === e.WEEKLY ? (i.recurrenceFrequency = r.weekly.recurrenceFrequency,
            i.recurrenceDaysOfWeek = [],
            r.weekly.monday && i.recurrenceDaysOfWeek.push("Mon"),
            r.weekly.tuesday && i.recurrenceDaysOfWeek.push("Tue"),
            r.weekly.wednesday && i.recurrenceDaysOfWeek.push("Wed"),
            r.weekly.thursday && i.recurrenceDaysOfWeek.push("Thu"),
            r.weekly.friday && i.recurrenceDaysOfWeek.push("Fri"),
            r.weekly.saturday && i.recurrenceDaysOfWeek.push("Sat"),
            r.weekly.sunday && i.recurrenceDaysOfWeek.push("Sun")) : i.recurrenceType === e.MONTHLY ? (i.recurrenceAbsolute = r.monthly.recurrenceAbsolute,
            i.recurrenceAbsolute ? (i.recurrenceFrequency = r.monthly.absolute.recurrenceFrequency,
            i.recurrenceDayOfMonth = r.monthly.absolute.recurrenceDayOfMonth) : (i.recurrenceFrequency = r.monthly.relative.recurrenceFrequency,
            i.recurrenceWeekOfMonth = r.monthly.relative.recurrenceWeekOfMonth,
            i.recurrenceDayOfWeek = r.monthly.relative.recurrenceDayOfWeek)) : i.recurrenceType === e.YEARLY && (i.recurrenceAbsolute = r.yearly.recurrenceAbsolute,
            i.recurrenceAbsolute ? (i.recurrenceMonthOfYear = r.yearly.absolute.recurrenceMonthOfYear,
            i.recurrenceDayOfMonth = r.yearly.absolute.recurrenceDayOfMonth) : (i.recurrenceDayOfWeek = r.yearly.relative.recurrenceDayOfWeek,
            i.recurrenceWeekOfMonth = r.yearly.relative.recurrenceWeekOfMonth,
            i.recurrenceMonthOfYear = r.yearly.relative.recurrenceMonthOfYear))
        }
        ;
        this.save = function() {
            i.startTime = i.allDay ? null  : i.startTime,
            i.endTime = i.allDay ? null  : i.endTime,
            s()
        }
        ,
        this.recurrence = r,
        this.timeline = i

        return this;
    };

    var getTimelineLabel = function(timeline){
      var t = {}
      , n = {
        DAILY: "Daily",
        WEEKLY: "Weekly",
        MONTHLY: "Monthly",
        YEARLY: "Yearly"
    }
      , i = {
        EVERY_DAY: "Every Day",
        ALL_DAY: "All Day",
        START: "Start",
        END: "End",
        TO: "to",
        DAY: "Day",
        OF: "Of",
        EVERY: "Every"
    }
      , r = ["First", "Second", "Third", "Fourth", "Last"]
      , a = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      , o = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
      , s = function(t, n, i) {
        var r = ""
          , a = new Date(t);
        return n ? (a.setMinutes(a.getMinutes() + a.getTimezoneOffset()),
        r = e("date")(a, i)) : r = e("date")(a, i),
        r
    };




    };

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

//        //var date = new Date(parseInt(datetime));
//        var localeSpecificTime = datetime.toLocaleTimeString();
//        return localeSpecificTime.replace(/:\d+ /, ' ');


return{
    getTimeline : getTimeline
    ,getTimelineRecurrenceWise : getTimelineRecurrenceWise
    ,getTimelineLabel : getTimelineLabel
    ,getOnlyTime : getOnlyTime
    ,getOnlyDate : getOnlyDate
    ,getDateTimeFromDate : getDateTimeFromDate
    ,getDateTimeFromTime : getDateTimeFromTime
}

}]);

sdApp.factory('timelineDescription',['$filter','timelineFactory', function(e, tLF){
var t = {}
      , n = {
        DAILY: "DAILY",
        WEEKLY: "WEEKLY",
        MONTHLY: "MONTHLY",
        YEARLY: "YEARLY"
    }
      , i = {
        EVERY_DAY: "Every Day",
        ALL_DAY: "All Day",
        START: "Start",
        END: "End",
        TO: "to",
        DAY: "Day",
        OF: "Of",
        EVERY: "Every"
    }
      , r = ["First", "Second", "Third", "Fourth", "Last"]
      , a = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      , o = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
      , s = function(t, n, i) {
        var r = ""
          , a = new Date(t);
        return n ? (a.setMinutes(a.getMinutes() + a.getTimezoneOffset()),
        r = e("date")(a, i)) : r = e("date")(a, i),
        r
    };

    var updateLabel = function(e) {
        var t = ""
          , l = "dd-MMM-yyyy";

        //if timedefined => is_always.
        if(e.timeDefined){
            t = t + "Always";
        }
        else
        {
            //if for only single day, then consider date only once.
            //set Hours is to compare only the date part and to avoid time comparision
            if(e.startDate.setHours(0,0,0,0) == e.endDate.setHours(0,0,0,0)){
                t = t+tLF.getOnlyDate(e.startDate) + ' ';
            }
            else{
                t = t+tLF.getOnlyDate(e.startDate) + ' ';
                t = t + i.TO + " " + tLF.getOnlyDate(e.endDate) + " "
            }
            if(e.allDay){
                t = t + i.ALL_DAY;
            }else{
                var c = "hh:mm a";
                    t = t + tLF.getOnlyTime(e.startTime) + " ",
                    e.endTime && (t = t + i.TO + " " + tLF.getOnlyTime(e.endTime) + " ")
            }
        }
        
        //set Hours is to compare only the date part and to avoid time comparision
        if (e.recurrenceType && e.startDate.setHours(0,0,0,0) != e.endDate.setHours(0,0,0,0)) {
            var u = 0;
            if (t = t + e.recurrenceType + " ",
            e.recurrenceType === n.MONTHLY && (e.recurrenceAbsolute ? (t = t + i.DAY + " " + e.recurrenceDayOfMonth + " " + i.OF + " ",
            u = e.recurrenceFrequency) : (t = t + r[e.recurrenceWeekOfMonth] + " " + a[e.recurrenceDayOfWeek] + " " + i.OF + " ",
            u = e.recurrenceFrequency)),
            t = t + i.EVERY + " ",
            t = e.recurrenceType === n.YEARLY ? e.recurrenceAbsolute ? t + o[e.recurrenceMonthOfYear] + " " + e.recurrenceDayOfMonth + " " : t + r[e.recurrenceWeekOfMonth] + " " + a[e.recurrenceDayOfWeek] + " " + i.OF + " " + o[e.recurrenceMonthOfYear] + " " : t + e.recurrenceFrequency + " " + e.recurrenceType.substring(0, e.recurrenceType.length - 2).replace("i", "y") + "(s) ",
            e.recurrenceType === n.WEEKLY && e.recurrenceDaysOfWeek)
                for (var d = 0; d < e.recurrenceDaysOfWeek.length; d++)
                    "Mon" === e.recurrenceDaysOfWeek[d] ? t = t + a[1] + " " : "Tue" === e.recurrenceDaysOfWeek[d] ? t = t + a[2] + " " : "Wed" === e.recurrenceDaysOfWeek[d] ? t = t + a[3] + " " : "Thu" === e.recurrenceDaysOfWeek[d] ? t = t + a[4] + " " : "Fri" === e.recurrenceDaysOfWeek[d] ? t = t + a[5] + " " : "Sat" === e.recurrenceDaysOfWeek[d] ? t = t + a[6] + " " : "Sun" === e.recurrenceDaysOfWeek[d] && (t = t + a[0] + " ")
        }
        return t
    };

    return{
        updateLabel : updateLabel
    }

}]);

sdApp.controller('timelinetextboxController',['$scope', '$uibModal','$log','timelineFactory','timelineDescription',
 function($scope, $uibModal, $log, timelineFactory, timelineDescription){

    //private methods
    var onLoad = function(){
        $scope.timeline = timelineFactory.getTimeline(
            $scope.timeDefined
            ,timelineFactory.getDateTimeFromDate($scope.startDate)
            ,timelineFactory.getDateTimeFromDate($scope.endDate)
            ,$scope.allDay
            ,timelineFactory.getDateTimeFromTime($scope.startTime)
            ,timelineFactory.getDateTimeFromTime($scope.endTime)
            ,$scope.recurrenceType
            ,$scope.recurrenceFrequency
            ,$scope.recurrenceAbsolute
            ,$scope.recurrenceDayOfMonth
            ,$scope.recurrenceWeekOfMonth
            ,$scope.recurrenceDaysOfWeek
        );
        updateTimeLabel();
        //$log.log($scope.timeline);
        updateTimelineObjects($scope.timeline);
    };

    var updateTimelineObjects = function(timeline){
            $scope.timeDefined = timeline.timeDefined
            ,$scope.startDate= timelineFactory.getOnlyDate(timeline.startDate)
            ,$scope.endDate=timelineFactory.getOnlyDate(timeline.endDate)
            ,$scope.allDay = timeline.allDay
            ,$scope.startTime=timelineFactory.getOnlyTime(timeline.startTime)
            ,$scope.endTime=timelineFactory.getOnlyTime(timeline.endTime)
            ,$scope.recurrenceType=timeline.recurrenceType
            ,$scope.recurrenceFrequency=timeline.recurrenceFrequency
            ,$scope.recurrenceAbsolute=timeline.recurrenceAbsolute
            ,$scope.recurrenceDayOfMonth=timeline.recurrenceDayOfMonth
            ,$scope.recurrenceWeekOfMonth=timeline.recurrenceWeekOfMonth
            ,$scope.recurrenceDaysOfWeek=timeline.recurrenceDaysOfWeek;
    }

    var updateTimeLabel = function(){
         $scope.label = timelineDescription.updateLabel($scope.timeline);
    }

    $scope.$watch('timeDefined', function(newValue){
        $scope.timeline.timeDefined = newValue;
        updateTimeLabel()
    });

    $scope.openTimelineModal=function(){
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/static/templates/scheduleManagement/_timeline_modal.html',
          controller: 'timelineModalController',
          size: 'lg'
          ,backdrop: 'static' //disables modal closing by click on the backdrop.
          ,resolve: {
            timeline: function(){
                return angular.copy($scope.timeline);
            }
          }
        });

        modalInstance.result.then(function apply(timeline) {
            $scope.timeline = timeline
            updateTimelineObjects(timeline);

            toastr.success('timeline updated');
            $scope.label = timelineDescription.updateLabel($scope.timeline);

            }, function cancel() {
                toastr.warning('cancelled');
            });
    }

    onLoad();
}]);

sdApp.controller('timelineModalController',['$scope','$uibModalInstance','timeline', '$log','timelineFactory',
 function($scope, $uibModalInstance, timeline, $log, timelineFactory){
    var r = new timelineFactory.getTimelineRecurrenceWise(timeline);
    $scope.timeline=r.timeline;
    $scope.recurrence = r.recurrence;

    //date
    $scope.popUp1dateOptions = {
            dateDisabled: false,
            formatYear: 'yy',
            maxDate: new Date(2020, 5, 22),
            minDate: new Date(),
            startingDay: 1
            ,showWeeks : false
        };
    $scope.popUp2dateOptions = {
            dateDisabled: false,
            formatYear: 'yy',
            maxDate: new Date(2020, 5, 22),
            minDate: $scope.timeline.startDate,
            startingDay: 1
            ,showWeeks : false
        };
    $scope.format = 'dd-MMMM-yyyy';
    $scope.openDatepicker = function(datetype){
        if(datetype == 'startDate' )
        {
            $scope.popUp1.opened = true;
        }
        else
        {
            $scope.popUp2.opened = true;
            $log.log($scope.timeline.startDate);
            $log.log($scope.popUp2dateOptions);

        }
    }

    $scope.popUp1 = { opened : false };
    $scope.popUp2 = { opened : false };

    $scope.$watch('timeline.startDate', function(newValue, oldValue){
        $scope.popUp2dateOptions.minDate = newValue;
    });

    //time


    $scope.apply = function () {
        if($scope.timeline.endDate < $scope.timeline.startDate)
        {
            alert('end date should be more than start date')
        }
        else{
            r.save();
            $uibModalInstance.close($scope.timeline);
            $log.log($scope.timeline);
        }

    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };



}]);

sdApp.directive("largerThanDate", [function() {
        return {
            require: "ngModel",
            link: function(e, t, n, i) {
                e.$watchGroup(["timeline.startDate", "timeline.endDate"], function(e) {
                    var startDate = e[0] && new Date(e[0])
                      , endDate = e[1] && new Date(e[1])
                      , r = !(startDate && endDate && startDate > endDate);
                    i.$setValidity("largerThanDate", r)
                })
            }
        }
    }
]);

sdApp.directive("largerThanTime", [function() {
        return {
            require: "ngModel",
            link: function(e, t, n, i) {
                e.$watchGroup(["timeline.startTime", "timeline.endTime"], function(e) {
                    var startTime = e[0] && new Date(e[0])
                      , endTime = e[1] && new Date(e[1])
                      , r = !(startTime && endTime && startTime >= endTime);
                    i.$setValidity("largerThanTime", r)
                });
            }
        }
    }
]);

//**end timline material

//distribution list material
sdApp.directive('distributionList', function(){
    return{
        restrict : 'E'
        ,scope : {
            selectedScreens : '='
            ,selectedGroups : '='
        }
        ,controller : 'distributionListController'
        ,templateUrl : '/static/templates/scheduleManagement/_distribution_list.html'
        ,link : function($scope, elements, attr){

        }
    }
});

sdApp.controller('distributionListController',['$scope', '$uibModal','$log',
 function($scope, $uibModal, $log){

    $scope.openDistributionSelectorModal = function(){
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/static/templates/scheduleManagement/_distribution_selector_modal.html',
          controller: 'distributionSelectorController',
          size: 'lg'
          ,backdrop: 'static' //disables modal closing by click on the backdrop.
          ,resolve: {
            selectedScreens: function(){
                return angular.copy($scope.selectedScreens);
            }
            ,selectedGroups : function(){
                return angular.copy($scope.selectedGroups)
            }
          }
        });

        modalInstance.result.then(function apply(selectedList){
            $scope.selectedScreens= angular.copy(selectedList.screens);
            $scope.selectedGroups = angular.copy(selectedList.groups);
            $log.log($scope.selectedGroups);
            $log.log($scope.selectedScreens);
        }, function cancel(){
            toastr.warning('cancelled');
        })
    };

    $scope.removeScreen=function(index){
        $scope.selectedScreens.splice(index,1);
        toastr.success('screen Removed')
    };
    $scope.removeGroup=function(index){
        $scope.selectedGroups.splice(index,1);
        toastr.success('group Removed');
    }
}]);

sdApp.factory('distributionSelectorFactory', ['$log', '$http', '$q','scheduleDetailsFactory',
 function($log, $http, $q, sDF){

    //private methods
    var getScreensJson = function(callback){
        $http({
            method : "GET",
            url : "/api/screen/getScreens"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };

    var getGroupsJson = function(callback){
         $http({
            method : "GET",
            url : "/api/screen/getGroups"
        }).then(function mySucces(response) {
            if(callback)
            {
                callback(response.data);
            }
        }, function myError(response) {
            console.log(response.statusText);
        });
    };


    //public methods
    var getScreensListWithSelectedBool = function(selectedScreens, callback){
        getScreensJson(function(allScreens){
            var allScreensWithSelectedBool = sDF.selectedBoolSetter(allScreens, selectedScreens, 'screen_id',
             'schedule_screen_id');
            callback(allScreensWithSelectedBool);
        });
    };

    var getGroupsListWithSelectedBool = function(selectedGroups, callback){
        getGroupsJson(function(allGroups){
            var allGroupsWithSelectedBool = sDF.selectedBoolSetter(allGroups, selectedGroups, 'group_id'
            ,'schedule_screen_id');
            callback(allGroupsWithSelectedBool);
        });
    };

    var getSelectedItems = function(allItems){
        var selectedItems = sDF.getSelectedItems(allItems);
        return selectedItems;
    }

    return{
        getScreensListWithSelectedBool : getScreensListWithSelectedBool
        ,getGroupsListWithSelectedBool : getGroupsListWithSelectedBool
        ,getSelectedItems : getSelectedItems
    }

}]);

sdApp.controller('distributionSelectorController',['$scope','$uibModalInstance', '$log','selectedScreens',
 'selectedGroups','distributionSelectorFactory',
  function($scope,$uibModalInstance, $log, selectedScreens, selectedGroups, dSF){

//private methods
var onLoad = function(){
    dSF.getScreensListWithSelectedBool(selectedScreens, function(data){
        $scope.allScreens = data;
    });
    dSF.getGroupsListWithSelectedBool(selectedGroups, function(data){
        $scope.allGroups = data;
    });
};

//public methods
$scope.apply = function(){
    var selectedScreens = dSF.getSelectedItems($scope.allScreens);
    var selectedGroups = dSF.getSelectedItems($scope.allGroups);
    var selectedItems = {
        screens : selectedScreens,
        groups : selectedGroups
    };
    $uibModalInstance.close(selectedItems);
};
$scope.cancel = function(){
    $uibModalInstance.dismiss();
}

onLoad();

 }]);
//**end-distribution list material


//playlistsList material

sdApp.directive('playlistTextbox',['$uibModal', function($uibModal){
    return{
        restrict:'E'
        ,scope : {
            selectedPlaylists : '='
            ,selectedWidgets : '='
            ,selectedBlynqPlaylists : '='
        }
        ,templateUrl : '/static/templates/scheduleManagement/_playlist_textbox.html'
        ,link : function($scope, elements,attr){
            $scope.removePlaylist = function(index){
                $scope.selectedPlaylists.splice(index,1);
            };
            $scope.removeWidget = function(index){
                $scope.selectedWidgets.splice(index,1);
            }
            $scope.removeBlynqContent = function(index){
                $scope.selectedBlynqPlaylists = [];
            };
            $scope.openPlaylistSelectorModal = function(){
                var modalInstance = $uibModal.open({
                  animation: true,
                  templateUrl: '/static/templates/scheduleManagement/_playlist_selector_modal.html',
                  controller: 'playlistSelectorController',
                  size: 'lg'
                  ,backdrop: 'static' //disables modal closing by click on the backdrop.
                  ,resolve: {
                    resolvedObj : function(){
                        var resolvedObj = {};
                        resolvedObj.selectedPlaylists = angular.copy($scope.selectedPlaylists);
                        resolvedObj.selectedBlynqPlaylists = angular.copy($scope.selectedBlynqPlaylists);
                        resolvedObj.selectedWidgets = angular.copy($scope.selectedWidgets);
                        return resolvedObj
                    }
                    ,selectedWidgets: function(){
                        return angular.copy($scope.selectedWidgets);
                    }
                  }
                });
                modalInstance.result.then(function apply(appliedObjs){
                    $scope.selectedPlaylists= appliedObjs.selectedPlaylists;
                    $scope.selectedBlynqPlaylists = appliedObjs.selectedBlynqPlaylists;
                    $scope.selectedWidgets = appliedObjs.selectedWidgets;
                }, function cancel(){
                    toastr.warning('cancelled');
                });
            };
        }
    };
}]);

sdApp.factory('playlistSelectorFactory', ['scheduleDetailsFactory','$http','plDataAccessFactory','$q',
 function(sDF, $http, pDF, $q){
    //private functions

    var getWidgetsJson = function(callback){
        $http({
             method : "GET",
             url : '/api/playlist/getWidgetPlaylists'
         }).then(function mySucces(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    //public functions
    var getPlaylistsListWithSelectedBool = function(selectedPlaylists, callback){
        pDF.getPlaylists(function(allPlaylists){
            var allPlaylistsWithSelectedBool = sDF.selectedBoolSetter(allPlaylists,selectedPlaylists, 'playlist_id'
            ,'schedule_playlist_id');
            callback(allPlaylistsWithSelectedBool);
        })
    };


    var getWidgetsListWithSelectedBool = function(selectedWidgets, callback){
        getWidgetsJson(function(allWidgets){
            var allWidgetsWithSelectedBool = sDF.selectedBoolSetter(allWidgets, selectedWidgets, 'playlist_id'
            , 'schedule_playlist_id');
            callback(allWidgetsWithSelectedBool);
        })
        }

    var getBlynqContentWithSelectedBool = function(selectedBlynqPlaylists){
        var deferred = $q.defer();
        sDF.getBlynqPlaylists().then(function(allBlynqPlaylists){
            var allCategoriesWithSelectedBool = sDF.selectedBoolSetter(allBlynqPlaylists, selectedBlynqPlaylists, 'playlist_id'
            ,'schedule_playlist_id');
            deferred.resolve(allCategoriesWithSelectedBool);
        });

        return deferred.promise
    };

    var getSelectedItems = function(allItems){
        var selectedItems = sDF.getSelectedItems(allItems);
        return selectedItems;
    }

    return{
        getPlaylistsListWithSelectedBool : getPlaylistsListWithSelectedBool
        ,getWidgetsListWithSelectedBool : getWidgetsListWithSelectedBool
        ,getSelectedItems : getSelectedItems
        ,getBlynqContentWithSelectedBool : getBlynqContentWithSelectedBool
    }
}]);


sdApp.controller('playlistSelectorController', ['$scope', '$log','$uibModalInstance','resolvedObj',
'playlistSelectorFactory', function($scope, $log, $uibModalInstance, resolvedObj, pSF){
    var onLoad = function(){
        pSF.getPlaylistsListWithSelectedBool(resolvedObj.selectedPlaylists,function(data) {
            $scope.allPlaylists = data;
        });
        pSF.getWidgetsListWithSelectedBool(resolvedObj.selectedWidgets, function(data) {
            $scope.allWidgets = data;
        });

        pSF.getBlynqContentWithSelectedBool(resolvedObj.selectedBlynqPlaylists).then(function(data){
            $scope.allBlynqPlaylists = data;
        });
    };

    $scope.apply = function(){
        var returnObj ={};
        returnObj.selectedPlaylists = angular.copy(pSF.getSelectedItems($scope.allPlaylists));
        returnObj.selectedBlynqPlaylists = angular.copy(pSF.getSelectedItems($scope.allBlynqPlaylists));
        returnObj.selectedWidgets=angular.copy(pSF.getSelectedItems($scope.allWidgets));
        $uibModalInstance.close(returnObj);
    };
    $scope.cancel = function(){
        $uibModalInstance.dismiss();
    }

    onLoad();
}]);

//**end playlists List material


//calenders - Schedule
sdApp.factory('calendarFactory',[function(){
    var calendarViewTypes = {
        day : 'day'
        ,week : 'week'
        ,month : 'month'
        ,year : 'year'
    }
    return{
        calendarViewTypes : calendarViewTypes
    }
}])
//**end calenders -Schedule


//add schedule
sdApp.directive('addSchedule',['$log','scheduleIndexFactory','$uibModal','blueprints','scheduleDetailsFactory',
    'playlistSelectorFactory','$q',
    function($log, sIF, $uibModal,blueprints,sDF,pSF,$q){
    return{
        restrict    :   'EA'
        ,scope      :   {
            refreshSchedules : '&refreshSchedulesFn'
        }
//        ,template:   '<a class="btn  btn-primary pull-right" ng-click="addSchedule()">\
//                        <i class="fa fa-plus"></i> \
//                        Add Schedule\
//                        </a>'
        ,link : function($scope, elem){
                var openModalPopup = function(index){
                    var newSchedule = new blueprints.Schedule();

                    var layoutsProm = sDF.getDefaultLayouts();
                    if(false){
                        var defaultBlynqPlaylistsProm =  sDF.getDefaultBlynqPlaylists();
                    }

                    $q.all([
                        layoutsProm.then(function(layouts){
                            newSchedule.layout = angular.copy(layouts[0]);
                            newSchedule.schedule_panes.push(new blueprints.SchedulePane(layouts[0].layout_panes[0]));})
//                      ,defaultBlynqPlaylistsProm.then(function(allPlaylists){
//                          newSchedule.schedule_panes[0].schedule_blynq_playlists = angular.copy(allPlaylists);
//                       });
                    ])
                    .then(function(){
                        var modalInstance = $uibModal.open({
                          animation: true,
                          templateUrl: '/static/templates/scheduleManagement/schedule_details.html',
                          controller: 'scheduleDetailsCtrl',
                          size: 'lg'
                          ,backdrop: 'static' //disables modal closing by click on the backdrop.
                          ,resolve: {
                            schedule: function(){
                                return newSchedule
                            }
                          }
                        });
                        modalInstance.result.then(function saved(){
                            $scope.refreshSchedules();
                        }, function cancelled(){
                            toastr.warning('schedule cancelled')
                        });
                    });





                };

                elem.on('click', function(){
                    openModalPopup();
                })
        }
    }
}]);

//*end Add schedule