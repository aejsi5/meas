"use strict";
var dev_mode = true;
var employee = null;
var employeeid = null;
var n_empl = {};
var token = Cookies.get('csrftoken');

jQuery(document).ready(function ($) {
    addSpinner();
    let searchParams = new URLSearchParams(window.location.search);
    if(searchParams.has('employeeid')){
        employeeid = searchParams.get('employeeid');
        //fill form with employee-data
        let csrf_token = Cookies.get('csrftoken');
        let url = window.location.protocol + "//" + window.location.host + '/api/v1/employee/' + employeeid;
        if(employeeid=="new"){
            $('#id_emplacn').prop('disabled',false);
            $('#id_emplacn').removeClass('form-control-plaintext');
            $('#id_emplacn').addClass('form-control input-req');
            $('#AccountnumberHelpBlock').removeClass('hide');
            $('#id_empledit_cancel').prop('disabled', true);
            $('#id_empledit_delete').prop('disabled', true);
            rmSpinner();
        }else{
            ajax_call(csrf_token, url, null, 'GET');
        }
    } else {
        status_code_handler(404);
        window.setTimeout('window.location = "/mitarbeiter"', 2000);
    }
    start_event_listener();
});
function fill_form(){
    $('#id_emplacn').val(employee.Employees_acn);
    $('#id_emplfirst').val(employee.Employees_first);
    $('#id_empllast').val(employee.Employees_last);
    $('#id_emplbd').val(employee.Employees_birthday);
    $('#id_emplphone').val(employee.Employees_phone);
    $('#id_emplemail').val(employee.Employees_mail);
    $('#id_emplvf').val(datetimeconverter(employee.Employees_vf));
    if (employee.Employees_vu != null){
        $('#id_emplvu').val(datetimeconverter(employee.Employees_vu));
    }
    rmSpinner();
};

function input_cleaner(str, fieldtype){
    str = str.replace('<','');
    str = str.replace('>', '');
    str = str.replace('!', '');
    str = str.replace('"', '');
    str = str.replace('§', '');
    str = str.replace('%', '');
    str = str.replace('&', '');
    str = str.replace('/', '');
    str = str.replace('(', '');
    str = str.replace(')', '');
    str = str.replace('=', '');
    if(!fieldtype=='mail'){
        str = str.replace('@', '');
    };
    str = str.replace('€', '');
    str = str.replace(',', '');
    str = str.replace(';', '');
    str = str.replace('#', '');
    str = str.replace("'", '');
    str = str.replace('{', '');
    str = str.replace('}', '');
    str = str.replace('[', '');
    str = str.replace(']', '');
    if (!fieldtype == 'phone') {
        str = str.replace('+', '');
    };
    str = str.replace('*', '');
    return str
};

function form_saveable(with_status_code_handler){
    if (!$('#id_emplacn').val()){
        console.log("ACN empty");
        return false;
    }
    if (!$('#id_emplfirst').val()){
        if(with_status_code_handler==true){
            status_code_handler(4001);
            console.log("First empty");
            return false;
        } else {
            console.log("First empty");
            return false
        }
    }
    if (!$('#id_empllast').val()){
        if (with_status_code_handler == true) {
            status_code_handler(4002);
            console.log("Last empty");
            return false;
        } else {
            console.log("Last empty");
            return false
        }
    }
    if ($('#id_emplbd').val()){
        let input = new Date($('#id_emplbd').val());
        let today = Date.now();
        if (input >= today){
            if (with_status_code_handler == true) {
                status_code_handler(4003);
                console.log("BD not valid");
                return false;
            } else {
                console.log("BD not valid");
                return false
            }
        }
    }
    if ($('#id_emplphone').val()){
        var pattern = new RegExp($('#id_emplphone').attr("pattern"));
        if (!pattern.test($('#id_emplphone').val())){
            if (with_status_code_handler == true) {
                status_code_handler(4004);
                console.log("Phone not valid");
                return false;
            } else {
                console.log("Phone not valid");
                return false
            }
        }
    }
    if (!$('#id_emplemail').val()){
        if (with_status_code_handler == true) {
            status_code_handler(4005);
            console.log("Mail not valid");
            return false;
        } else {
            console.log("Mail not valid");
            return false;
        }
    } 
    if (!$('#id_emplvf').val()) {
        if (with_status_code_handler == true) {
            status_code_handler(4006);
            console.log("Validate not valid");
            return false;
        }else {
            console.log("Validate not valid");
            return false;
        };
    };
    return true;
};

function collector(){
    if(employeeid=='new'){
        if ($('#id_emplacn').val() === "") {
            n_empl.Employees_acn = null;
        } else {
            n_empl.Employees_acn = input_cleaner($('#id_emplacn').val(), 'text');
        };
    } else {
        n_empl.Employees_acn = employee.Employees_acn;
    };
    if ($('#id_emplfirst').val()===""){
        n_empl.Employees_first = null;
    }else{
        n_empl.Employees_first = input_cleaner($('#id_emplfirst').val(), 'text');
    };
    if ($('#id_empllast').val() === "") {
        n_empl.Employees_last = null;
    } else {
        n_empl.Employees_last = input_cleaner($('#id_empllast').val(), 'text');
    };
    if ($('#id_emplbd').val() === "") {
        n_empl.Employees_birthday = null;
    } else {
        n_empl.Employees_birthday = input_cleaner($('#id_emplbd').val(), 'date');
    };
    if ($('#id_emplphone').val() === "") {
        n_empl.Employees_phone = null;
    } else {
        n_empl.Employees_phone = input_cleaner($('#id_emplphone').val(), 'phone');
    };
    if ($('#id_emplemail').val() === "") {
        n_empl.Employees_mail = null;
    } else {
        n_empl.Employees_mail = input_cleaner($('#id_emplemail').val(), 'mail');
    };
    if ($('#id_emplvf').val() === "") {
        n_empl.Employees_vf = null;
    } else {
        n_empl.Employees_vf = input_cleaner($('#id_emplvf').val(), 'datetime');
    };
    if ($('#id_emplvu').val() === "") {
        n_empl.Employees_vu = null;
    } else {
        n_empl.Employees_vu = input_cleaner($('#id_emplvu').val(), 'datetime');
    };
    if (!employeeid == 'new') {
        n_empl.Mandant = employee.Mandant;
    }
}

function datetimeconverter(datetimestring){
    var date = new Date (datetimestring);
    var y = date.getFullYear();
    var m = ('0' + (date.getMonth() + 1)).slice(-2);
    var d = ('0' + date.getDate()).slice(-2);
    var h = ('0' + date.getHours()).slice(-2);
    var min = ('0' + date.getMinutes()).slice(-2);
    return y + '-' + m + '-' + d + 'T' + h + ':' + min
}

function start_event_listener(){
    $('.input-empledit-form').change(function () {
        if (!$(this).val() == "" && $(this).prop('required')) {
            $(this).removeClass('input-req');
        };
        if ($(this).val() == "" && $(this).prop('required')) {
            $(this).addClass('input-req');
        };
        if (form_saveable(false) == true) {
            $('.btn-employeeedit').prop('disabled', false);
        };
        if (form_saveable(false) == false) {
            $('#id_empledit_save').prop('disabled', true);
        };
    });
    $('.input-empledit-form').keydown(function () {
        if(!$(this).val()=="" && $(this).prop('required')){
            $(this).removeClass('input-req');
        };
        if ($(this).val() == "" && $(this).prop('required')) {
            $(this).addClass('input-req');
        };
        if (form_saveable(false) == true) {
            $('.btn-employeeedit').prop('disabled', false);
        };
        if (form_saveable(false) == false) {
            $('#id_empledit_save').prop('disabled', true);
        };
    });
    $('#id_button_empledit_cancel').click(function(){
        event.preventDefault();
        if (!$('#id_button_empledit_cancel').is(':disabled')){
            fill_form();
            $('.btn-employeeedit').prop('disabled', true);
        }
    });
    $('#id_empledit_save').click(function () {
        if (!$('#id_button_empledit_save').is(':disabled')) {
            collector();
            var token = Cookies.get('csrftoken');
            let url = window.location.protocol + "//" + window.location.host + '/api/v1/employee/' + employeeid;
            if(form_saveable(true)==true && employeeid!='new'){
                ajax_call(token, url, n_empl, 'PUT');
            }
            if (form_saveable(true) == true && employeeid == 'new') {
                let url_new = window.location.protocol + "//" + window.location.host + '/api/v1/employee/';
                ajax_call(token, url_new, n_empl, 'POST');
            }
            else {
                status_code_handler(999);
            };
        };
    });
    $('#id_button_empledit_delete').click(function(){
        event.preventDefault();
        //var token = Cookies.get('csrftoken');
        if(employee.Employees_id != employeeid){
            status_code_handler(404);
            return
        } else {
            Swal.fire({
                title: 'Möchten Sie den ausgewählten Datensatz wirklich löschen?',
                text: "Dies kann nicht rückgängig gemacht werden",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Fortfahren',
                cancelButtonText: 'Abbrechen',
                focusCancel: true
            }).then((result) => {
                if(result.value){
                    let url = window.location.protocol + "//" + window.location.host + '/api/v1/employee/' + employeeid;
                    ajax_call(token, url,null,'DELETE');
                };
            });
        };
    });
};

function ajax_call(csrf, api_url = "", api_data, api_method) {
    if (api_method == 'GET') {
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            success: function (result, status, xhr) {
                employee = result;
                fill_form();
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    }
    if (api_method == 'DELETE') {
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            success: function (result, status, xhr) {
                status_code_handler(202);
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    };
    if (api_method == 'PUT') {
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(api_data),
            success: function (result, status, xhr) {
                status_code_handler(200);
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    };
    if (api_method == 'POST') {
        $.ajax({
            headers: { "X-CSRFToken": csrf },
            type: api_method,
            url: api_url,
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(api_data),
            success: function (result, status, xhr) {
                status_code_handler(201);
                window.location = '/mitarbeiter/edit/?employeeid=' + result.Employees_id
            },
            error: function (result, status, xhr) {
                status_code_handler(result.status);
            },
            timeout: 120000,
        });
    };
};

function status_code_handler(statuscode) {
    switch (statuscode) {
        case 200:
            Toast.fire({
                icon: 'success',
                title: 'Änderung gespeichert',
            });
            $('.btn-employeeedit').prop('disabled', true);
            break;
        case 201:
            Toast.fire({
                icon: 'success',
                title: 'Datensatz angelegt',
            });
            $('.btn-employeeedit').prop('disabled', true);
            break;
        case 202:
            Toast.fire({
                icon: 'success',
                title: 'Datensatz gelöscht',
                text: 'Sie werden in Kürze weitergeleitet'
            });
            window.setTimeout('window.location = "/mitarbeiter"', 1000);
            break;
        case 403:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Sie haben nicht die erforderlichen Rechte'
            });
            break;
        case 404:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Datensatz nicht gefunden'
            });
            break;
        case 4001:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Vorname ist ein Pflichtfeld'
            });
            break;
        case 4002:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Nachname ist ein Pflichtfeld'
            });
            break;
        case 4003:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Der Geburtstag kann nicht in der Zukunft liegen'
            });
            break;
        case 4004:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Telefonnummer hat das falsche Format'
            });
            break;
        case 4005:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Email ist ein Pflichtfeld'
            });
            break
        case 4006:
            Toast.fire({
                icon: 'error',
                title: 'Transaktion fehlgeschlagen',
                text: 'Bitte geben Sie an, ab wann der Datensatz gültig sein soll'
            });
            break
        default:
            Toast.fire({
                icon: 'error',
                title: 'Es ist ein unbekannter Fehler aufgetreten',
                text: 'Bitte versuchen Sie es später noch einmal'
            });
    };
};