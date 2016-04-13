var PageLoad = (function(){

    function onPageload()
    {
        $('.ms-container-wrap .list-group').sortable(
            {
                containment : '.ms-container-wrap',
                connectWith  : '.list-group'
            }
        );
    }

    return{
        onPageload : onPageload
    }

})();


var PageUtil = (function(){

    function animateListItem($event)
    {
        $li = $($event.target).closest('li');

        $li.animate({
             height: '-=5px', width:'-=5px'}, "fast");
        $li.animate({
            height: '+=5px', width:'+=5px'}, "fast");
    }

    return{
        animateListItem : animateListItem
    }
})();

var ScheduleManagement = (function(){

    function listItemClicked($event){
         PageUtil.animateListItem($event);

         $li = $($event.target);
         if($li.hasClass('selected')){
            $li.removeClass('selected');
         }
         else{
            $li.addClass('selected');
         }
    }

    return{
        listItemClicked : listItemClicked
    }
})();

$(function(){

    //set active Tab in Side Navigation bar
    $('.side-navbar ul .nav-1').addClass('active');

    //onPageload
    PageLoad.onPageload();

    //animate on select
    $('.ms-list-container').on('click','li', ScheduleManagement.listItemClicked);


});