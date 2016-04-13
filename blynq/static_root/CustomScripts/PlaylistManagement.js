var PageLoad = (function(){

    //Private functions

    //public functions
    function onPageLoad()
    {
        PageUtil.putPlaylistEditModeOff();
    }
return{
    onPageLoad:onPageLoad
};
})();

var PageUtil = (function(){

    //private functions
    function getNewPlayListItem(ui){
        var itemType = ui.draggable.find('.item-container').data('itemtype');
        var itemId = ui.draggable.find('.item-container').data('itemid');
        var itemName = ui.draggable.find('.item-container-header').html();

        var newListItem='somestring';
        switch(itemType)
        {
            case 'image':
                newListItem = '<li class="list-group-item hover" data-itemid="' + itemId +'" data-mins="01" data-secs="00">' +itemName+
                                            '<span class="glyphicon glyphicon-remove pull-right edit-mode"></span> \
                                            <span class="glyphicon glyphicon-time pull-right edit-mode"></span> \
                                            </li>';
        }
        return newListItem;
    }

    //public functions
    function enableSortable()
    {
        $('#divPlaylistItems .list-group').sortable({
            containment : "parent"
        });
    }

    function disableSortable()
    {
        $( "#divPlaylistItems .list-group" )
            .sortable( "option", "disabled", true );
    }

    function enableDraggable()
    {
        $('.div-draggable-wrap').draggable({
            helper: 'clone'
            //,connectToSortable : '#divPlaylistItems'
            //,revert : true
        }
        );
    }

    function disableDraggable()
    {
        $('.div-draggable-wrap')
            .draggable("option", "disabled", true);
    }

    function enableDroppable()
    {
        $("#divPlaylistItems").droppable({
              accept : '.div-draggable-wrap'
              ,hoverClass : 'highlight-acceptable'
              ,drop: function(event, ui){
                    var newPlaylistItem = getNewPlayListItem(ui);
                    $('#divPlaylistItems .list-group').append(newPlaylistItem);
                    toastr.success('Item Added to Playlist');
                }
            });
    }

    function disableDroppable()
    {
        $("#divPlaylistItems")
            .droppable("option", "disabled", true);
    }

    function putPlaylistEditModeOn()
    {
        $('#divPlaylistItems').find('.edit-mode').show();
        $('#divPlaylistItems').find('.save-mode').hide();
    }

    function putPlaylistEditModeOff()
    {
        $('#divPlaylistItems .edit-mode').hide();
        $('#divPlaylistItems .save-mode').show();
    }


return{
    enableSortable:enableSortable,
    disableSortable:disableSortable,
    enableDraggable: enableDraggable,
    disableDraggable : disableDraggable,
    enableDroppable :enableDroppable,
    disableDroppable : disableDroppable,
    putPlaylistEditModeOn : putPlaylistEditModeOn,
    putPlaylistEditModeOff : putPlaylistEditModeOff
};
})();

var PlaylistManagement = (function(){

    //private functions
    function ValidatePlaylistItemTimeForm(){
        $('#div-mdl-playlistItem-timeDuration').validator('validate');
    }

    function UpdatePlaylistItemElementDataValues(){

    }

    function AddPlaylist(){
        toastr.success('Playlist added successfully');
    }

    function getPlaylistitems(playListId){
        //ajax call to get and display the playlist items
    }

    function getPlaylists(){
        //ajax call to get and display the playlist items
    }




    //PlayList
    function playlistSelected($event){
        var $listItem = $($event.target);
        var activePlaylist =  $('#divPlaylists li .active').data('playlistid');
        var selectedPlaylist = $listItem.data('playlistid');

        if(activePlaylist != selectedPlaylist)
        {
            //update the active class
            $('#divPlaylists li').removeClass('.active');
            $listItem.addClass('.active');

            //ajax call to get the playlistItems for the selected playlist.
        }
    }

    function deletePlaylistRequested($event){
        var $listItem = $($event.target).closest('li');
        $listItem.remove();
    }

    function AddNewItem($event){
        $event.preventDefault();
        var $divItemsContainer = $($event.target).closest('.items-container');
        //remove any existing validation styles
        $divItemsContainer.find('.div-add-item').validator('validate');
        hideAddItemDiv($divItemsContainer.find('.div-add-item'));
        AddPlaylist();
    }

    function cancelAddNewItem($event){
        $event.preventDefault();
        var $divItemsContainer = $($event.target).closest('.items-container');
        $divItemsContainer.find('.div-add-item input:text').each(function(){
            $(this).val('');
        })

        //
        $divItemsContainer.find('.div-add-item').hide();
        toastr.warning('New playlist not saved');
    }

    function DisplayAddItemDiv($event){
        var $divItemsContainer = $($event.target).closest('.items-container');
        $divItemsContainer.find('.div-add-item').show();
    }

    function hideAddItemDiv($div)
    {
        $div.hide();
    }


    //Playlistitems
    function displayTimeSettingDialog($event){
        var $listItem = $($event.target).closest('li');
        var activePlaylist = $('#divPlaylists ul .active');

        $('#div-mdl-playlistItem-timeDuration').modal();
        //open dialog
    }

    function removePlaylistItem($event){
        var $listItem = $($event.target).closest('li');
        $listItem.remove();
        toastr.success('Item removed from playlist');
    }

    function submitPlaylistItemTime($event){
        //validate form --
        ValidatePlaylistItemTimeForm();
        //save values to that element

        // close the modal
    }



    function editPlaylist(){
        PageUtil.putPlaylistEditModeOn();
        PageUtil.enableSortable();
        PageUtil.enableDraggable();
        PageUtil.enableDroppable();
    }

    function savePlaylist(){
        PageUtil.putPlaylistEditModeOff();
        toastr.success('Playlist saved');

    }

    function cancelPlaylistSave(){
        PageUtil.putPlaylistEditModeOff();
        PageUtil.disableSortable();
        PageUtil.disableDraggable();
        PageUtil.disableDroppable();

        // reload the playlistItems
        var playlistId = parseInt($('.divPlaylists li.active').data('playlistid'),10);
        getPlaylistitems(playlistId);

        toastr.warning('playlist updates not saved');
    }

return{
    displayTimeSettingDialog:displayTimeSettingDialog,
    playlistSelected: playlistSelected,
    removePlaylistItem : removePlaylistItem,
    submitPlaylistItemTime : submitPlaylistItemTime,
    AddNewItem : AddNewItem,
    DisplayAddItemDiv: DisplayAddItemDiv,
    editPlaylist : editPlaylist,
    savePlaylist : savePlaylist,
    cancelPlaylistSave : cancelPlaylistSave,
    cancelAddNewItem : cancelAddNewItem,
    deletePlaylistRequested : deletePlaylistRequested
};
})();

$(function(){
    $('.side-navbar ul .nav-3').addClass('active');

    //addPlaylist
    $('.lnk-add-item').on('click', PlaylistManagement.DisplayAddItemDiv);
    $('.submit-additem').on('click', PlaylistManagement.AddNewItem);
    $('.cancel-additem').on('click', PlaylistManagement.cancelAddNewItem);

    //editPlaylist
    $('#divPlaylistItems').on('click','.save-mode', PlaylistManagement.editPlaylist);
    $('#divPlaylistItems').on('click','.div-header .glyphicon-ok', PlaylistManagement.savePlaylist);
    $('#divPlaylistItems').on('click', '.div-header .glyphicon-remove', PlaylistManagement.cancelPlaylistSave);

    //deletePlaylist
    $('#divPlaylists').on('click', '.glyphicon-trash', PlaylistManagement.deletePlaylistRequested);

    //getthePlaylistitems
    $('#divPlaylists').on('click','ul li', PlaylistManagement.playlistSelected);

    //set the timing for each item
    $('#divPlaylistItems')
        .on('click', '#lst-playlistitems li .glyphicon-time', PlaylistManagement.displayTimeSettingDialog)
        .on('click', '#lst-playlistitems li .glyphicon-remove', PlaylistManagement.removePlaylistItem);

    // submitPlaylistItemTime
    $('#div-mdl-playlistItem-timeDuration').on('click', '#submitPlaylistItemTime', PlaylistManagement.submitPlaylistItemTime);




    //on pageload
    PageLoad.onPageLoad();

});