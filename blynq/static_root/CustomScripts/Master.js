

var PageUtil = (function(){

//private variables
var activeTab = 0;
var Tabs = ['nav-0', 'nav-1', 'nav-2', 'nav-3', 'nav-4','nav-5'];

function setActiveTab($event){
    var selectedTab = $($event.target).closest('li').attr('class');

if(selectedTab != Tabs[activeTab])
{
    //remove active class
    $('.'+Tabs[activeTab]).removeClass('active');

    //add active class
    $('.'+selectedTab).addClass('active');

    //split the selectedTab to get the number
    activeTab = parseInt(selectedTab.split('-')[1]);
}
}

return{
//alertMessage:alertMessage,
setActiveTab:setActiveTab
};

})();

function displayDialogueModal(heading, bodyContent, okFunction, NeedClose, CloseFunction){
    $dialogueBox = $('#modal-DialogueBox')
    $dialogueBox.find('.modal-title').text(heading);
    $dialogueBox.find('.modal-bodytext').text(bodyContent)
    $()

}

$(function(){
    $('.vertical-leftfloat-5').on('click','.navbar-nav li',PageUtil.setActiveTab);

});
