var PageUtil = (function(){
return{
};
})();

var ScreenManagementActions = (function(){
    //private functions
    function AddGroup(){
        var newGroupName = $('#txtGroupName').val().trim();
        if(newGroupName == "")
        {
            $('#txtGroupName').parent().addClass('has-error');
            $('#txtGroupName').focus();
        }
        else{
            //ajax call
        }
    }

    function AddScreen(){
        var proceed = ValidateScreenNameAndActivationKey();
        if(proceed)
        {
        //ajax call
        }
    }

    function ValidateScreenNameAndActivationKey()
    {
        var newScreenName = $('#txtScreenName').val().trim();
        var activationKey = $('#txtActivationKey').val();

        if(newScreenName =="")
        {
            $('#txtScreenName').parent().addClass('has-error');
            $('#txtScreenName').focus();
            return false;
        }
        if(activationKey == "")
        {
            $('#txtActivationKey').parent().addClass('has-error');
            $('#txtActivationKey').focus();
            return false;
        }
        return true;
    }

    function DisplayAddItemDiv($event)
    {
        var $divItemsContainer = $($event.target).closest('.items-container');
        $divItemsContainer.find('.div-add-item').show();
    }

    function AddNewItem($event){
        $event.preventDefault();
        //remove any existing validation styles
        $($event.target).closest('.items-container').find('.form-group').each(function(){
            $(this).removeClass('has-error')
        })

        var itemType = $($event.target).closest('.items-container').data('itemtype');
        if(itemType == 'Group')
        {
            AddGroup();
        }
        else
        {
            AddScreen();
        }
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


return{
    DisplayAddItemDiv:DisplayAddItemDiv,
    AddNewItem : AddNewItem,
    cancelAddNewItem : cancelAddNewItem
};
})();

$(function(){
        //set active Tab in Side Navigation bar
        $('.side-navbar ul .nav-4').addClass('active');

        $('.lnk-add-item').on('click', ScreenManagementActions.DisplayAddItemDiv);
        $('.submit-additem').on('click', ScreenManagementActions.AddNewItem);
        $('.cancel-additem').on('click', ScreenManagementActions.cancelAddNewItem);

        $('.list-group').sortable({cursor : 'pointer'});

});