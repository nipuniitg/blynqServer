/*var ctApp = angular.module('ctApp',['as.sortable']).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
    });*/

plApp.factory('ctDataAccessFactory',['$http','$window', function($http,$window){

    var deleteContent = function(content_ids, callback){
        var postData = {
            content_ids : content_ids
        };
        $http({
             method : "POST"
             ,url : '/api/content/deleteContent'
             ,data : postData
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var getFilesJson = function(folderId, callback){
        var URL = '/api/content/getFilesJson/'+ folderId;
        $http({
             method : "GET",
             url : URL
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var getFoldersJson = function(folderId, callback){
        var URL = '/api/content/getFoldersJson/'+ folderId;
        $http({
             method : "GET",
             url : URL
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var createFolder = function(currentFolderId, mdlObj, callback){
        postData ={};
        postData.currentFolderId = currentFolderId;
        postData.title = mdlObj.title;
        $http({
             method : "POST",
             url : '/api/content/createFolder',
             data : postData
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var updateContentTitle = function(contentObj, callback){
        $http({
             method : "POST",
             url : '/api/content/updateContentTitle',
             data : contentObj
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var getFolderPath = function(folderId, callback){
        $http({
             method : "GET"
             ,url : '/api/content/folderPath/'+ folderId
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    };

    var moveContent = function(content_ids, parent_folder_id, callback){
        var postData ={
            content_ids : content_ids
            ,parent_folder_id : parent_folder_id
        };
        $http({
             method : "POST",
             url : '/api/content/moveContent',
             data : postData
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var upsertUrl = function(content, parent_folder_id, callback ){
        var postData = {};
        postData.content = content;
        postData.parent_folder_id = parent_folder_id;
        $http({
             method : "POST",
             url : '/api/content/upsertUrl',
             data : postData
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    var getValidContentTypes = function(callback){
        $http({
             method : "GET"
             ,url : '/api/content/validContentTypes'
         }).then(function mySuccess(response){
                if(callback)
                {
                    callback(response.data);
                }
            }, function myError(response) {
                console.log(response.statusText);
            });
    }

    return{
        deleteContent : deleteContent
        ,getFiles : getFilesJson
        ,getFolders : getFoldersJson
        ,createFolder : createFolder
        ,updateContentTitle : updateContentTitle
        ,getFolderPath : getFolderPath
        ,moveContent    :   moveContent
        ,upsertUrl  : upsertUrl
        ,getValidContentTypes : getValidContentTypes
    }

}]);

//Any logic that needs some computation goes here.
plApp.factory('ctFactory', ['ctDataAccessFactory', function(ctDataAccessFactory){

    // These are used by the playlist controller.
    var folders =null;
    var files = null;


    var getFolders = function(folderId, callback)
    {
        ctDataAccessFactory.getFolders(folderId,function(data)
        {
            folders = data;
            callback(data)
        });
    };

    var getFiles = function(folderId, callback)
    {
        ctDataAccessFactory.getFiles(folderId,function(data)
        {
            files = data;
            callback(data)
        });
    };

    var getFoldersObj = function()
    {
        return folders;
    };

    var getFilesObj = function()
    {
        return files;
    };

    return{
        getFolders : getFolders
        ,getFiles : getFiles
        ,getFoldersObj : getFoldersObj
        ,getFilesObj : getFilesObj
    }

}]);

plApp.controller('ctCtrl',['$scope','ctFactory','ctDataAccessFactory', '$uibModal',
function($scope, ctFactory, ctDataAccessFactory, $uibModal ){

    //private functions
    var onLoad = function(){
        $scope.currentFolderId = -1  //-1 represents root folder. And hence fetches the data in root folder.
        $scope.refreshContent($scope.currentFolderId);

//        $uibTooltip.options=
//            {
//                'popover-append-to-body' : true,
//                'popover-trigger' : 'mouseenter'
//            }
//        ;
    };

    var getCheckedContentItems = function(){
        if($scope.checkedFolders.length > 0 || $scope.checkedContent.length >0)
        {
            var content_ids =[];
            for(i=0;i<$scope.checkedFolders.length;i++)
            {
                content_ids.push($scope.folders[$scope.checkedFolders[i]].content_id);
            }
            for(i=0;i<$scope.checkedContent.length;i++)
            {
                content_ids.push($scope.files[$scope.checkedContent[i]].content_id);
            }
            return content_ids;
        }
        else{
            toastr.warning('Check atleast one item to complete the action');
            return false;
        }
    }

    $scope.fileIcons = {
        pdf : '/static/images/pdf_logo.png'
        ,video : '/static/images/video_icon.png'
        ,folder : '/static/images/folder-icon.png'
        ,url : '/static/images/url_icon.png'
    };

    $scope.refreshContent = function(folderId){

        ctFactory.getFolders(folderId, function(data)
        {
            $scope.folders = data;
        });

        ctFactory.getFiles(folderId, function(data)
        {
            $scope.files = data;
        });

        clearCheckedLists();

        updateFolderPath(folderId);

    };

    var updateFolderPath = function(folderId){
        ctDataAccessFactory.getFolderPath(folderId, function(data){
            $scope.folderPath = data
            $scope.currentFolderId = folderId;
        });
    };

    //public or Scope releated functions
    $scope.deleteSingleContent = function(content_id){
        ctDataAccessFactory.deleteContent([content_id],  function(data){
            if(data.success)
            {
                $scope.refreshContent($scope.currentFolderId);
                toastr.success('Item deleted successfully.');
            }
            else{
                toastr.warning("Oops!!There was some error. Please try later.");
            }
        });
    };

    $scope.deleteMultipleContents = function(){
        var content_ids = getCheckedContentItems();
        if(content_ids){
            ctDataAccessFactory.deleteContent(content_ids, function(data){
                if(data.success)
                {
                    $scope.refreshContent($scope.currentFolderId);
                    toastr.success('Items deleted successfully.');
                }
                else{
                    toastr.warning("Oops!!There was some error. Please try later.");
                }
            })
        }
    }

    $scope.navigateToFolder = function(folderId){
        $scope.refreshContent(folderId);
    };

    //----createFolderfunctions
    $scope.createFolder = function(){
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/contentManagement/_create_folder_mdl.html'
              ,size: 'md'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve :{
                currentFolderId : function(){
                    return $scope.currentFolderId
                }
              }
              ,controller: function($scope, $uibModalInstance, ctDataAccessFactory, currentFolderId){
                  var onLoad = function(){
                    $scope.folderObj = {};
                    $scope.folderObj.title = '';
                  }
                  $scope.create = function(){
                        ctDataAccessFactory.createFolder(currentFolderId, $scope.folderObj, function(data){
                            if(data.success)
                            {
                                toastr.success('Folder created Successfully');
                                $uibModalInstance.close();
                            }
                            else{
                                toastr.warning('Oops!!There was some error while creating folder. Please try again.');
                            }
                        });
                  }

                  $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                  }

                  onLoad();
              }
        });

        modalInstance.result.then(function folderCreated(){
            $scope.refreshContent($scope.currentFolderId);
        }, function cancelled(){

        });

    }
    //----createFolderfunctions


    //----editContentTitle

    $scope.editContent= function(content, index){
        if(content.content_type == 'url'){
            $scope.editUrl(index);
        }else{
            editTitle();
        }
    }

    var editTitle = function(content){
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/contentManagement/_edit_content_title_mdl.html'
              ,size: 'md'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve :{
                contentObj : function(){
                    return angular.copy(content)
                }
              }
              ,controller: function($scope, $uibModalInstance, ctDataAccessFactory, contentObj){
                  var onLoad = function(){
                    $scope.content = contentObj
                  }
                  $scope.update = function(){
                        ctDataAccessFactory.updateContentTitle($scope.content, function(data){
                            if(data.success)
                            {
                                toastr.success('Title modified successfully');
                                $uibModalInstance.close();
                            }
                            else{
                                toastr.warning('Oops!! Some error occured while updating the template');
                            }
                        });
                  }

                  $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                  }

                  onLoad();
              }
        });

        modalInstance.result.then(function titleUpdated(){
            $scope.refreshContent($scope.currentFolderId);
        }, function cancelled(){

        });
    }



    //move item
    var clearCheckedLists = function(){
        $scope.checkedFolders = [];
        $scope.checkedContent =[];
    }

    $scope.toggleCheck = function(type, index){
        if(type=='folder'){
            var idx = $scope.checkedFolders.indexOf(index)
            if (idx > -1) {
              $scope.checkedFolders.splice(idx, 1);
            }

            // is newly selected
            else {
              $scope.checkedFolders.push(index);
            }
        }
        else{
            var idx = $scope.checkedContent.indexOf(index)
            if (idx > -1) {
              $scope.checkedContent.splice(idx, 1);
            }

            // is newly selected
            else {
              $scope.checkedContent.push(index);
            }
        }
    }

    $scope.moveContent = function(){
        var content_ids = angular.copy(getCheckedContentItems());
        if(content_ids){
            var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/contentManagement/_move_content_mdl.html'
              ,controller: 'mdlContentMoveCtrl'
              ,size: 'lg'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    content_ids : function(){
                        return content_ids
                    }
              }
            });

            modalInstance.result.then(function moveTo(newParentId){
                ctDataAccessFactory.moveContent(content_ids, newParentId, function(returnData){
                    if(returnData.success){
                        toastr.success('Content Moved Successfully.');
                        $scope.refreshContent($scope.currentFolderId);
                    }
                    else{
                        toastr.warning('Oops! Some error occured while moving. Please try again later.')
                    }

                });
            }, function cancelled(){
                toastr.warning('Move cancelled')
            });
        }
    };


    //view Content
    $scope.viewContentInDetail = function(file){
        var modalInstance = $uibModal.open({
              animation: true
              //,backdrop : false
              ,templateUrl: '/static/templates/contentManagement/_content_view_mdl.html'
              ,controller: 'mdlContentInDetailCtrl'
              ,size: 'lg'
              ,windowTemplateUrl : '/static/templates/shared/_mdl_window_template.html'
              //,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    file : function(){
                        return file
                    }
              }
            });

        modalInstance.result.then(function ok(newParentId){

        }, function cancelled(){

        });
    }

    //upload
    $scope.upload = function(){
        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/contentManagement/_upload_mdl.html'
              ,controller: 'mdlUploadContentCtrl'
              ,size: 'md'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    parentScopeObj : function(){
                        return {
                            currentFolderId : $scope.currentFolderId
                        }
                    }
              }
            });

        modalInstance.result.then(function uploaded(){
            $scope.refreshContent($scope.currentFolderId);
        }, function cancelled(){
        });
    }

    //upsertURl
    var newURL = -1;

    $scope.addNewURL = function(){
        openUpsertURLModal(newURL);
    }

    $scope.editUrl = function(index){
        openUpsertURLModal(index);
    }

    var openUpsertURLModal = function(index){
        var isNewURL = index == newURL ? !0 : !1;

        var modalInstance = $uibModal.open({
              animation: true
              ,templateUrl: '/static/templates/contentManagement/_url_mdl.html'
              ,size: 'md'
              ,backdrop: 'static' //disables modal closing by click on the backdrop.
              ,resolve : {
                    urlObj : function(){
                        if(isNewURL)
                        {
                            return {
                                content_id : -1
                                ,title : ''
                                ,url : ''
                            }
                        }
                        else{
                            return angular.copy($scope.files[index]);
                        }
                    }
                    ,currentFolderId : function(){
                        return $scope.currentFolderId
                    }
              }
              ,controller : function($scope, $uibModalInstance,ctDataAccessFactory, urlObj,currentFolderId,$log){
                    var isNewURL;
                    var onLoad = function(){
                        $scope.urlObj = urlObj;
                        isNewURL = urlObj.content_id == -1 ? !0 : !1
                        if(isNewURL){
                            $scope.modalTitle = 'Add URL';
                            $scope.saveVerbose = 'Add';
                        }
                        else{
                            $scope.modalTitle = 'Update URL';
                            $scope.saveVerbose = 'Update';
                        }
                    }
                    onLoad();

                    var validate = function(){
                        if($scope.urlUpsertForm.$valid){
                            return !0
                        }else{ return !1}
                    }

                    $scope.save = function(){
                        if(validate()){
                            ctDataAccessFactory.upsertUrl($scope.urlObj, currentFolderId, function(returnData){
                                if(returnData.success){
                                    if(isNewURL){
                                        toastr.success('url Added Successfully');
                                    }else{
                                        toastr.success('url updated Successfully');
                                    }
                                    $uibModalInstance.close();
                                }else{
                                    toastr.warning('Oops! some error occured while '+ (isNewURL ? 'adding.':'updating.')
                                    +'Please try after refreshing the page');
                                    $log.log(returnData.errors);
                                }
                            })
                        }else{
                            toastr.warning('There are some error in the form. Please correct them');
                        }
                    }

                    $scope.cancel = function(){
                        $uibModalInstance.dismiss();
                    }
              }
            });

        modalInstance.result.then(function saved(){
            $scope.refreshContent($scope.currentFolderId);
        }, function cancelled(){
        });
    }

    onLoad();
}]);

plApp.controller('mdlContentMoveCtrl', ['content_ids','$scope','$uibModalInstance','ctDataAccessFactory',
 function(content_ids,$scope,$uibModalInstance, ctDAF){

    var onLoad = function(){
        $scope.currentFolderId = -1;
        refreshFolders($scope.currentFolderId);
        updateFolderPath($scope.currentFolderId);
    };

    var refreshFolders = function(content_id){
        ctDAF.getFolders(content_id, function(returnData){
            $scope.folders = returnData;
        });
    };

    var updateFolderPath = function(folderId){
        ctDAF.getFolderPath(folderId, function(data){
            $scope.folderPath = data
            $scope.currentFolderId = folderId;
        });
    };

    $scope.navigateToFolder = function(folderId){
        refreshFolders(folderId);
        updateFolderPath(folderId);
    };

    var validateErrors = function(){
        var idx = content_ids.indexOf($scope.currentFolderId);
        if(idx > -1)
        {
            return true
        }
        else{
            return false
        }
    }

    $scope.moveHere = function(){
        if(validateErrors()){
            toastr.error('You are trying to move folder into itself. Please re-check');
        }
        else{
            $uibModalInstance.close($scope.currentFolderId);
        }
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss('cancel');
    }

    onLoad();
 }]);

plApp.controller('mdlContentInDetailCtrl',['$scope','file','$uibModalInstance',
 function($scope, file, $uibModalInstance){

    var onLoad = function(){
        $scope.file = file;
    };

    onLoad();

}]);

plApp.controller('mdlUploadContentCtrl', ['$scope','$uibModalInstance', 'parentScopeObj','$cookies','ctDataAccessFactory',
 function($scope,$uibModalInstance, parentScopeObj, $cookies, ctDAF){
    var validateFiles = [];
    var onLoad = function(){
        $scope.currentFolderId = parentScopeObj.currentFolderId;
        $scope.files=[];
        $scope.uploadProgressIndicator = 0;
        ctDAF.getValidContentTypes(function(returnData){
            validFileTypes = returnData
        })

    };

   // var validFileTypes = ['image/png','image/jpg','image/jpeg','image/gif','application/pdf','video/mp4','video/mkv'];

    $scope.validateFiles = function(){
        $scope.invalidFiles = [];
        var invalid = false;
        if($scope.files.length>0)
        {
            for(var i in $scope.files){
                if(validFileTypes.indexOf($scope.files[i].type)<0)
                {
                    $scope.$apply(function(){$scope.invalidFiles.push($scope.files[i])});
                    invalid = true;
                }

            }
            if(invalid){
                toastr.warning('There are some invalid files.Please remove them and try again');
                return false
            }
            else{
                return true
            }
        }else{
            toastr.warning('Select atleast one file');
            return false
        }

    }

    $scope.uploadFiles = function(){
        if($scope.validateFiles())
        {
            var formData = new FormData();
            var filesArr = [];

            for(var i in $scope.files){
                formData.append('file'+i, $scope.files[i]);
            }
            formData.append('currentFolderId', $scope.currentFolderId);
            formData.append('totalFiles', $scope.files.length);


            // ADD LISTENERS.
            var objXhr = new XMLHttpRequest();
            var csrftoken = $cookies.get('csrftoken');
            //using upload is necessary. It triggers the progress bar.
            objXhr.upload.onprogress = updateProgress;
            objXhr.addEventListener("load", transferComplete, false);

            // SEND FILE DETAILS TO THE API.
            objXhr.open("POST", "/api/content/uploadContent/");
            objXhr.setRequestHeader("X-CSRFToken", csrftoken);
            objXhr.send(formData);
        }
    }

    var updateProgress = function(e){
        if(e.lengthComputable)
        {
            console.log(e.loaded + ',' + e.total +','+ e.lengthComputable);
            $scope.$apply(function(){
                $scope.uploadProgressIndicator = (e.loaded/e.total *100);
            });
        }
    };

    var transferComplete = function(){
        toastr.success('upload Complete');
        $uibModalInstance.close();
    };

    $scope.cancel = function(){
        $uibModalInstance.dismiss('cancel');
        toastr.warning('upload aborted');
    }

    onLoad();
}]);

plApp.directive('draggable', function(){
return{
    restrict : 'A',
    link: function(scope, element, attrs) {
        element.draggable({
            revert : 'invalid'
            ,helper: 'clone'
            /*,containment : 'section.wrapper'*/
            ,stack : '.div-draggable-wrap'
            ,snap : '#ul-playlistQueue'
            ,start : function(event, ui){
            }
            ,stop : function(event,ui){
            }
            ,appendTo:'body'
        });
        }
}});

plApp.directive('droppable', function(){
return{
    restrict : 'A'
    ,scope : {
        addContentFunction : '&addContentFunction'
        ,addFolderFunction : '&addFolderFunction'
    }
    ,link: function(scope, element, attrs) {
            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : 'highlight-acceptable'
              ,drop: function(event, ui){

                   var dragIndex = angular.element(ui.draggable).data('index');
                   var isFolder = angular.element(ui.draggable).data('isfolder');
                   if(isFolder){
                        scope.addFolderFunction()(dragIndex);
                   }
                   else
                   {
                        scope.addContentFunction()(dragIndex);
                   }

                }
            });

        }
}});

//content movement into folders
//maintains same scope.
plApp.directive('contentDroppable',['ctDataAccessFactory', function(ctDAF){
    return{
        restrict : 'A'
        ,link : function($scope, element,attrs){

            var postMomentFunction = function(returnData){
                if(returnData.success){
                    toastr.success('content Moved successfully');
                    $scope.refreshContent($scope.currentFolderId);
                }
                else{
                    toastr.warning(returnData.error);
                }
            };

            element.droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : 'highlight-acceptable'
              ,drop: function(event, ui){
                   var dragIndex = angular.element(ui.draggable).data('index');
                   var draggedisFolder = angular.element(ui.draggable).data('isfolder');
                   var dropIndex = attrs['index'];
                   if(draggedisFolder){
                        if(dragIndex != dropIndex){
                            ctDAF.moveContent([$scope.folders[dragIndex].content_id],
                            $scope.folders[dropIndex].content_id, postMomentFunction);
                        }
                        else{
                            toastr.warning('You cant move the folder into the same folder');
                        }
                   }
                   else
                   {
                        ctDAF.moveContent([$scope.files[dragIndex].content_id],
                         $scope.folders[dropIndex].content_id, postMomentFunction);
                   }
                }
            });
        }
    }
}]);

//Multiple File Upload directive
//maintains same scope
plApp.directive('fileUploadDtv', ['$log', function($log){
return{
    restrict : 'A'
    ,link : function($scope, elem, attrs){

            elem.bind('change', function(){
                $scope.files=[];
                $scope.$apply(function () {

                // STORE THE FILE OBJECT IN AN ARRAY.
                for (var i = 0; i < elem[0].files.length; i++) {
                    $scope.files.push(elem[0].files[i])
                }
                });
                $scope.validateFiles();
            });
    }
}
}]);

plApp.directive('pdfSection', ['PDFViewerService', function(pdf){
    return{
        restrict : 'E'
        ,link   : function($scope, elem, attr){
            $scope.viewer = pdf.Instance("viewer");

            $scope.nextPage = function() {
                $scope.viewer.nextPage();
            };

            $scope.prevPage = function() {
                $scope.viewer.prevPage();
            };

            $scope.pageLoaded = function(curPage, totalPages) {
                $scope.currentPage = curPage;
                $scope.totalPages = totalPages;
            };
        }
    }
}]);

plApp.filter('trusted', ['$sce', function ($sce) {
    return function(url) {
        return $sce.trustAsResourceUrl(url);
    };
}]);