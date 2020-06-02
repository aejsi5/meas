"use strict";
var dev_mode = true;


jQuery(document).ready(function ($) {
    start_event_listener();
});



function start_event_listener(){
    /*Adds the commands to edit or delete the employees data to the UI*/
    $(".ic-click-detail-menu").click(function () {
        $(".tool-detail-menu").not(".tool-detail-menu[data-emplid='" + $(this).data('emplid') + "']").addClass("no-show");
        $(".tool-detail-menu[data-emplid='" + $(this).data('emplid') + "']").toggleClass("no-show");
    });
    $('.tool-edit-cmd').click(function () {
        window.location = "/mitarbeiter/edit?employeeid=" + $(this).data('emplid');
    });
    $(".tool-delete-cmd").click(function () {
        $(".tool-detail-menu").addClass("no-show");
        let selection = $(this).data('emplid');
        var token = jQuery("[name=csrfmiddlewaretoken]").val();
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
            if (result.value) {
                let url = window.location.protocol + "//" + window.location.host + '/api/v1/employee/' + selection;
                ajax_call(token, url, null, 'DELETE');
                $(".col-sm[data-emplid='" + selection + "']").addClass('deleted');
                $(".overlay[data-emplid='" + selection + "']").addClass('blocking');
            };
        });
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
};

function status_code_handler(statuscode) {
    switch (statuscode) {
        case 200:
            Toast.fire({
                icon: 'success',
                title: 'Änderung gespeichert',
            });
            break;
        case 202:
            Toast.fire({
                icon: 'success',
                title: 'Datensatz gelöscht',
            });
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
        default:
            Toast.fire({
                icon: 'error',
                title: 'Es ist ein unbekannter Fehler aufgetreten',
                text: 'Bitte versuchen Sie es später noch einmal'
            });
    };
};