"use strict";
var dev_mode = true;
var domain = window.location.protocol + "//" + window.location.host

const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    onOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

jQuery(document).ready(function ($) {
    $('#id_menu_scheduler').click(function () {
        window.location = domain + '/terminplaner'
    });
    $('#id_menu_employee').click(function(){
        window.location = domain + '/mitarbeiter'
    });
    $('#id_menu_newemployee').click(function(){
        window.location = domain + '/mitarbeiter/edit/?employeeid=new'
    });
    $('#id_menu_customer').click(function(){
        window.location = domain + '/kunden'
    });
    $('#id_menu_product').click(function () {
        window.location = domain + '/material'
    });
    $('#id_menu_newcustomer').click(function () {
        window.location = domain + '/kunden/edit/?customerid=new'
    });
    $('#ic-logout').click(function () {
        window.location = '/logout';
    });
    $('.menu-sub').click(function () {
        $(this).toggleClass('menu-sub-act');
        $(this).siblings('.sub-menu').toggleClass('sub-menu-open');
    });
    $('.return-btn-span').hover(function(){
        $('.return-btn-span').tooltip('show')
    }, function(){
            $('.return-btn-span').tooltip('hide')
    });
    $('.return-btn-span').click(function(){
        window.history.go(-1);
    });
    $('.btn-upload-submit').click(function(){
        addSpinner();
    });
});


function status_code_handler(statuscode) {
    switch (statuscode) {
        case 200:
            Toast.fire({
                icon: 'success',
                title: 'Transaktion erfolgreich'
            });
            break;
        case 401:
            Toast.fire({
                icon: 'error',
                title: 'Authorisierung nicht erfolgreich',
                text: 'Bitte loggen Sie sich ein'
            });
            break;
        case 403:
            Toast.fire({
                icon: 'error',
                title: 'Zugriff verweigert',
                text: 'Sie haben nicht die erforderlichen Rechte '
            });
            break;
        case 404:
            Toast.fire({
                icon: 'error',
                title: 'Objeckt nicht gefunden'
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

function openNav() {
    $('.slidebar').width('280px');
    $('.menu').css('opacity', '1');
}
function closeNav() {
    $('.slidebar').width('0');
}
function addSpinner() {
    let spinner = '<div class="sk-fading-circle"><div class="sk-circle1 sk-circle"></div><div class="sk-circle2 sk-circle"></div><div class="sk-circle3 sk-circle"></div><div class="sk-circle4 sk-circle"></div><div class="sk-circle5 sk-circle"></div><div class="sk-circle6 sk-circle"></div><div class="sk-circle7 sk-circle"></div><div class="sk-circle8 sk-circle"></div><div class="sk-circle9 sk-circle"></div><div class="sk-circle10 sk-circle"></div><div class="sk-circle11 sk-circle"></div><div class="sk-circle12 sk-circle"></div></div>'
    $('main').append(spinner);
};
function rmSpinner() {
    $('.sk-fading-circle').fadeOut()
    window.setTimeout(function () {
        $('.sk-fading-circle').remove();
    }, 2000);
};

