var dataAccess = (function(){

    var siteHostName =   window.location.hostname ;
    //window.location.protocol + '//' + ':8000'

    function dAValidateCredentials(userName, password)
    {
        alert(siteHostName+'/ValidateCredentials');

        var values = {'userName': userName, 'password' : password};
        $.ajax({
            type: "GET",
            url:  '/ValidateCredentials',
            data: values,
            success: function (msg) {
                alert(msg);
                $('#inptest').val() = msg;
            },
            error: function (msg) {
                alert("Unable to Authenticate");
            }
        });
    }
    return{
        dAValidateCredentials: dAValidateCredentials
    };
})();

var pageSetup = (function(){

    function validateCredentials($event){
        var userName = $('#txtUsername').val();
        var password = $('#txtpassword').val();
        dataAccess.dAValidateCredentials(userName,password);
    }

    function NavigateToRegistrationPage($event){
        window.location.href = '/authentication/register'
    }

    return{
        validateCredentials: validateCredentials,
        NavigateToRegistrationPage:NavigateToRegistrationPage
    };

})();

$(document).ready(function() {
//    alert('js working');
    $('#divLoginFields').on('click','#btnRegister', pageSetup.NavigateToRegistrationPage);

}
);