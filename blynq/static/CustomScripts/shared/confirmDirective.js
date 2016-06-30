(function(){
'use strict';

angular.module('mainApp').directive('confirm', ['$log','$uibModal', function($log,$uibModal){
    var link = function($scope,elem,attr){
        elem.bind('click',function(){
            var modalInstance = $uibModal.open({
                  animation: true,
                  templateUrl: '/static/templates/shared/_confirm_modal.html',
                  controller: 'confirmDirectiveCtrl',
                  size: 'sm'
                  ,backdrop: 'static' //disables modal closing by click on the backdrop.
                  ,resolve: {
                    requiredVerbose: function(){
                        var requiredVerbose = {
                            modalTitle  : attr.modalTitle
                            ,message    : attr.message
                            ,confirmVerbose :   attr.confirmVerbose
                            ,cancelVerbose  :   attr.cancelVerbose
                        } ;
                        return requiredVerbose;
                    }
                  }
            });

            modalInstance.result.then(function(){
                $scope.confirmFn();
                }, function(){
                if($scope.cancelFn){
                    $scope.cancelFn();
                }
            });
        });
    }
    return{
        restrict    :   'A'
        ,scope : {
            confirmFn : '&'
            ,cancelFn  : '&'
        }
        ,compile : function compile(elem,attr){
            if(attr.confirmType && attr.confirmType=='delete')
            {
                attr.modalTitle = 'Warning';
                attr.confirmVerbose = 'Delete';
                attr.cancelVerbose = 'No';
                attr.message = 'Are you sure, you want to delete?'
            }
            else{
                if(!attr.modalTitle){attr.modalTitle = 'Warning'}
                if(!attr.confirmVerbose){attr.confirmVerbose = 'Ok'}
                if(!attr.cancelVerbose){attr.cancelVerbose = 'cancel'}
                if(!attr.message){attr.message = 'Are you sure?'}
            }

            return{
                post : link
            }
        }
    }
}]);

angular.module('mainApp').controller('confirmDirectiveCtrl', ['$scope','$uibModalInstance','requiredVerbose',
    function($scope,$uibModalInstance, requiredVerbose){

    $scope.modalTitle= requiredVerbose.modalTitle;
    $scope.message = requiredVerbose.message;
    $scope.confirmVerbose = requiredVerbose.confirmVerbose;
    $scope.cancelVerbose= requiredVerbose.cancelVerbose;


    $scope.ok = function(){
        $uibModalInstance.close($scope.timeline);
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss();
    };
}]);

}());
