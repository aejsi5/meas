"use strict";

jQuery(document).ready(function ($) {
    $('.menu-sub').click(function(){
        $(this).toggleClass('menu-sub-act');
        $(this).siblings('.sub-menu').toggleClass('sub-menu-open');
    });
});

function openNav(){
    $('.slidebar').width('280px');
    $('.menu').css('opacity', '1');
}
function closeNav() {
    $('.slidebar').width('0');
}
function addSpinner(){
    let spinner = '<div class="sk-fading-circle"><div class="sk-circle1 sk-circle"></div><div class="sk-circle2 sk-circle"></div><div class="sk-circle3 sk-circle"></div><div class="sk-circle4 sk-circle"></div><div class="sk-circle5 sk-circle"></div><div class="sk-circle6 sk-circle"></div><div class="sk-circle7 sk-circle"></div><div class="sk-circle8 sk-circle"></div><div class="sk-circle9 sk-circle"></div><div class="sk-circle10 sk-circle"></div><div class="sk-circle11 sk-circle"></div><div class="sk-circle12 sk-circle"></div></div>'
    $('main').append(spinner);
};
function rmSpinner() {
    $('.sk-fading-circle').fadeOut()
    window.setTimeout(function(){
        $('.sk-fading-circle').remove();
    },2000);
};


