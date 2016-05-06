var sdApp = angular.module("sdApp",['ui.bootstrap']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });

sdApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

//list of all the recent schedules
sdApp.controller('scheduleIndexCtrl', ['$scope', function($scope){


}]);

sdApp.controller('scheduleDetailsCtrl', ['$scope','$uibModal', function($scope, $uibModal){
    //schedule Details -screens/groups
    /*$scope.scheduleDetails.screens;
    $scope.scheduleDetails.playlist;
    $scope.scheduleDetails.timeline;*/

    $scope.openmodal = function(){
        var modalInstance = $uibModal.open({
          animation: false,
          //template : '<p>Hello</p>',
          templateUrl: '/templates/scheduleManagement/_timline_modal.html',
          //controller: 'ModalInstanceCtrl',
          size: 'lg',
          /*resolve: {
            items: function () {
              return $scope.items;
            }
          }*/
        });
    }

}]);

sdApp.directive('timelineTextbox', function(){
return{
    restrict: 'E'
    ,scope : {
        timeDefined :'='
        ,startDate :'='
        ,endDate :'='
        ,startTime :'='
        ,endTime :'='
        ,recurrenceType    :'='
        ,recurrenceFrequency  :'='
        ,recurrenceAbsolute    :'='
        ,recurrenceDayOfWeek   :'='
        ,recurrenceDayOfMonth  :'='
        ,recurrenceWeekOfMonth :'='
        ,recurrenceMonthOfYear :'='
        ,recurrenceDaysOfWeek  :'='
    }
    ,controller : 'timelinetextboxController'
    ,link : function($scope,element, attr){

    }
}
});

sdApp.controller('timelinetextboxController',['$scope', '$uibModal','$log', function($scope, $uibModal, $log){

    $scope.sometext = 'HI, this is from timeline contrller'
    $scope.openTimelineModal=function(){
        var modalInstance = $uibModal.open({
          animation: true,
          templateUrl: '/templates/scheduleManagement/_timeline_modal.html',
          controller: 'editTimelineController',
          size: 'lg'
          ,backdrop: 'static' //disables modal closing by click on the backdrop.
          ,resolve: {
            sometext: function(){
                return $scope.sometext;
            }
          }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            }, function () {

            });
    }
}]);

sdApp.controller('editTimelineController',['$scope','$uibModalInstance','sometext', '$log',
        function($scope, $uibModalInstance,sometext, $log ){
    $scope.sometext = sometext;
    $scope.timeline = {};


    //date
    $scope.timeline.startDate = new Date();
    $scope.timeline.endDate = null;
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
    $scope.

    $scope.apply = function () {
        if($scope.timeline.endDate < $scope.timeline.startDate)
        {
            alert('end date should be more than start date')
        }
        else{
            //$uibModalInstance.close($scope.selected.item);
            alert('applied');
        }

    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };



}]);