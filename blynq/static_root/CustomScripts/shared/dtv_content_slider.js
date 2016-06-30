(function(){
'use strict';

    angular.module('plApp').directive('contentSlider',['$uibModal', function($uibModal){
    return{
        restrict : 'AC'
        ,scope : {
            slideContent : '='
            ,index : '@'
        }
        ,link : function($scope, elem, attr){
            elem.bind('click', function(){
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
                            obj.slideContent = angular.copy($scope.slideContent);
                            if($scope.index){
                                obj.index = angular.copy(parseInt($scope.index));
                            }else{
                                obj.index = 0;
                            }

                            return obj;
                        }
                  }
                });
            })


        }
    }

    }]);


}());