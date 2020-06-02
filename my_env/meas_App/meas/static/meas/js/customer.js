"use strict";
var dev_mode = true;
var customer_id =null;


jQuery(document).ready(function ($) {
    var tbl = $('#customer_tbl').DataTable({
        responsive: true,
        stateSave: false,
        select:true,
        "info": true,
        "processing": true,
        "ordering": true,
        "searching": true,
        "language":{
            "emptyTable": "Keine Daten verfügbar",
            "info": "Angezeigt werden _START_ bis _END_ von _TOTAL_ Einträge",
            "infoEmpty": "Keine Daten verfügbar",
            "infoFiltered": "(gefiltert von _MAX_ Einträgen)",
            "thousands": ".",
            "lengthMenu": "_MENU_ Einträge pro Seite",
            "search": "Suche",
            "paginate": {
                "first": "Erste",
                "last": "Letzte",
                "next": "Vor",
                "previous": "Zurück"
            },
        },
        buttons: ['copy', 'excel'],
        ajax: {
            url: '/api/v1/customerlist/?format=json',
            dataSrc: 'data',
        },
        "columns": [
            {
                "data": 'Customer_id',
                "visible": false
            },
            {
                "data": 'Customer_acn',
                "title": "Kundennummer"
            },
            {
                "data": 'Customer_last',
                "title": "Nachname"
            },
            {
                "data": 'Customer_first',
                "title": "Vorname"
            },
            {
                "data": 'Customer_company',
                "title": "Firma"
            },
            {
                "data": 'Customer_street',
                "title": "Straße"
            },
            {
                "data": 'Customer_zip',
                "title": "PLZ"
            },
            {
                "data": 'Customer_city',
                "title": "Stadt"
            },
        ]
    });
    tbl.on('select', function (e, dt, type, indexes){
        if (type === 'row') {
            customer_id = tbl.rows(indexes).data().pluck('Customer_id');
            $('#id_cust_edit').prop('disabled', false);
        };
    });
    $('#id_cust_edit').click(function(){
        window.location = domain + '/kunden/edit/?customerid=' + customer_id[0]
    });
});





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