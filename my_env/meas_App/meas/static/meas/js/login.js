"use strict";
var dev_mode = true;

jQuery(document).ready(function ($) {
    
    $('#id_email').attr('placeholder', 'Email-Adresse');
    $('#id_new_password1').attr('placeholder', 'Neues Passwort');
    $('#id_new_password2').attr('placeholder', 'Bestätige Passwort');
    $("#id_login_submit").click(function(event){
        event.preventDefault();
        var CN = $('#login_input_CN').val();
        var UN = $('#login_input_UN').val();
        var PW = $('#login_input_PW').val();
        var token = Cookies.get('csrftoken');
        let data = {
            CustomerNumber: CN,
            UserName: UN,
            Password: PW
        };
        ajax_call(token, '/login/',data,'POST');
    }); 
});

function ajax_call(csrf, api_url="", api_data, api_method){
    if(api_data == null ){
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            success: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    }else{
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(api_data),
            success: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    };
};

function status_code_handler(statuscode){
    switch(statuscode){
        case 200:
            Toast.fire({
                icon: 'success',
                title: 'Anmeldung erfolgreich',
                text: 'Sie werden in Kürze weitergeleitet'
            });
            window.setTimeout('window.location = "/"', 2000);
            break;
        case 403:
            Toast.fire({
                icon: 'error',
                title: 'Anmeldung nicht erfolgreich',
                text: 'Bitte prüfen Sie Ihre Eingabe'
            });
            break;
        default:
            Toast.fire({
                icon: 'error',
                title: 'Es ist ein unbekannter Fehler aufgetreten',
                text: 'Bitte versuchen Sie es später noch einmal'
            });
    };
};




