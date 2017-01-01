/**
 * Created by zymxq on 2017/1/1.
 */
window.onload = function () {
    var log_h1 = document.querySelector('.log');
    var reg_h1 = document.querySelector('.reg');

    log_h1.onclick = function () {
        var forms = document.querySelectorAll('form');
        for(var i=0,len=forms.length;i < len;i++) {
            if (forms[i].id === 'login') {
                forms[i].classList.remove('hide');
                forms[i].classList.add('active');
            }
            else {
                forms[i].classList.remove('active');
                forms[i].classList.add('hide');
            }
        }
    };
    reg_h1.onclick = function () {
        var forms = document.querySelectorAll('form');
        for(var i=0,len=forms.length;i < len;i++) {
            if (forms[i].id === 'register') {
                forms[i].classList.remove('hide');
                forms[i].classList.add('active');
            }
            else {
                forms[i].classList.remove('active');
                forms[i].classList.add('hide');
            }
        }
    };
};