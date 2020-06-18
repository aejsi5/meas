"use strict";

function test(){
    var a = new Status()
    a.draw()
    window.setTimeout(function(){
        a.status_code = 0;
        a.draw();
    }, 2000);
    window.setTimeout(function () {
        a.status_code = 1;
        a.draw();
    }, 4000);
    window.setTimeout(function () {
        a.status_code = 2;
        a.draw();
    }, 6000);
    window.setTimeout(function () {
        a.status_code = 3;
        a.draw();
    }, 8000);
    window.setTimeout(function () {
        a.status_code = 4;
        a.draw();
    }, 10000);
    window.setTimeout(function () {
        a.status_code = 5;
        a.draw();
    }, 12000);
    window.setTimeout(function () {
        a.status_code = 6;
        a.draw();
    }, 14000);
    window.setTimeout(function () {
        a.status_code = 2;
        a.draw();
    }, 20000);
    window.setTimeout(function () {
        a.status_code = 6;
        a.draw();
    }, 22000);

}

class Status {
    constructor(status_code, history){
        this.status_code = status_code;
        if (history && history.hasOwnProperty('data')){
            this.his = history.data;
        } else {
            this.his = {};
        }
        if(status_code){
            this.his[this.status_code] = {
            'changed_at': Date.now(),
            'changed_by': 'Sie selbst'
            }
        }
    }

    print_currentstate(){
        console.log(this.status_code)
    }
    change(new_status_code){
        this.status_code = new_status_code;
        this.his[this.status_code] = {
            'changed_at': Date.now(),
            'changed_by': 'Sie selbst'
        }
        this.draw();
    }
    draw(){
        switch(this.status_code){
            case 0:
                //Created
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $("#state-label-created").removeClass('state-label-hidden');
                break
            case 1:
                //notyetscheduled
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $(".state-container-create").next().addClass('state-transition-active')
                $(".state-schedule").addClass('state-active shake');
                $("#state-label-notyetscheduled").removeClass('state-label-hidden');
                break
            case 2:
                //scheduled
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $(".state-container-create").next().addClass('state-transition-active')
                $(".state-schedule").addClass('state-completed');
                $("#state-label-scheduled").removeClass('state-label-hidden');
                break
            case 3:
                //in progress
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $(".state-container-create").next().addClass('state-transition-active')
                $(".state-schedule").addClass('state-completed');
                $(".state-container-schedule").next().addClass('state-transition-active')
                $(".state-inprogress").addClass('state-active rotating');
                $("#state-label-inprogress").removeClass('state-label-hidden');
                break
            case 4:
                //fullfilled
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $(".state-container-create").next().addClass('state-transition-active')
                $(".state-schedule").addClass('state-completed');
                $(".state-container-schedule").next().addClass('state-transition-active')
                $(".state-inprogress").addClass('state-completed');
                $(".state-container-inprogress").next().addClass('state-transition-active')
                $("#state-label-fullfilled").removeClass('state-label-hidden');
                break
            case 5:
                //completed
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-label").addClass('state-label-hidden');
                $(".state-create").addClass('state-completed');
                $(".state-container-create").next().addClass('state-transition-active')
                $(".state-schedule").addClass('state-completed');
                $(".state-container-schedule").next().addClass('state-transition-active')
                $(".state-inprogress").addClass('state-completed');
                $(".state-container-inprogress").next().addClass('state-transition-active')
                $(".state-complete").addClass('state-completed');
                $("#state-label-completed").removeClass('state-label-hidden');
                break
            case 6:
                //canceled
                $(".state-cycle").removeClass('rotating shake');
                $(".state-label").addClass('state-label-hidden');
                $(".state-complete").css('display', 'none');
                $(".state-cancel").css('display', 'flex');
                $("#state-label-canceled").removeClass('state-label-hidden');
                break
            default:
                //In Creation
                $(".state-cycle").removeClass('state-completed state-active rotating shake');
                $(".state-transition").removeClass('state-transition-active');
                $(".state-label").addClass('state-label-hidden');
                $(".state-cancel").css('display', 'none');
                $(".state-complete").css('display', 'flex');
                $(".state-create").addClass('state-active shake');
                $("#state-label-draft").removeClass('state-label-hidden');
                break
        }
    }
}