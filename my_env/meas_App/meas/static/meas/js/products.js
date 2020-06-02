"use strict";
var dev_mode = true;
var customer_id =null;

jQuery(document).ready(function ($) {
    var tbl = $('#products_tbl').DataTable({
        responsive: true,
        stateSave: false,
        select: true,
        "info": true,
        "processing": true,
        "ordering": true,
        "searching": true,
        "language": {
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
            url: '/api/v1/productlist/?format=json',
            dataSrc: 'data',
        },
        "columns": [
            {
                "data": 'Product_id',
                "visible": false
            },
            {
                "data": 'Product_number',
                "title": "Artikelnummer"
            },
            {
                "data": 'Product_name',
                "title": "Bezeichnung"
            },
            {
                "data": 'Product_supplier',
                "title": "Lieferant"
            },
            {
                "data": 'Product_unit.Unit_name',
                "title": "Einheit"
            },
            {
                "data": 'Product_sppu_net',
                "title": "Verkaufspreis netto"
            },
            {
                "data": 'Product_vf',
                "title": "Gültig von",
            },
            {
                "data": 'Product_vu',
                "title": "Gültig bis"
            },
        ]
    });
    tbl.on('select', function (e, dt, type, indexes) {
        if (type === 'row') {
            customer_id = tbl.rows(indexes).data().pluck('Customer_id');
            $('#id_cust_edit').prop('disabled', false);
        };
    });
    $('#id_cust_edit').click(function () {
        window.location = domain + '/kunden/edit/?customerid=' + customer_id[0]
    });
});







function status_code_handler(statuscode) {
    switch (statuscode) {
        case 200:
            Toast.fire({
                icon: 'success',
                title: 'Upload erfolgreich',
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