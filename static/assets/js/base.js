// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function toEnglishDigit(replaceString) {
    var find = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    var replace = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var regex;
    for (var i = 0; i < find.length; i++) {
        regex = new RegExp(find[i], "g");
        replaceString = replaceString.replace(regex, replace[i]);
    }
    return replaceString;
};


const regexIfNotEmpty = (input, regax = /^/) => {
    if (input.value !== '')
        return regax.test(toEnglishDigit(input.value));
    return true
}
const valid_persian_date = /^[0-9]{4}\/[0-9]{1,2}\/[0-9]{1,2}?$/,
    valid_email = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    valid_website = /(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/gi,
    valid_username = /^[a-zA-Z0-9]+$/;
$('form input[required]:not([type="hidden"]),form select[required],form textarea[required]').parent().append(`<span class="form-text text-muted"> الزامی </span>`)
$('form input:not(:required):not([type="hidden"]),form select:not(:required),form textarea:not(:required)').parent().append(`<span class="form-text text-muted"> اختیاری </span>`)

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-top-left",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "10000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};


const swalDelete = {
    title: 'آیا مطمئن هستید ؟',
    text: "رکورد پس از حذف قابل بازگشت نخواهد بود !",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#F64E60',
    cancelButtonColor: '#212121',
    confirmButtonText: 'بله! حذفش کن',
    cancelButtonText: 'لغو'
};
const swalFireError = (desc = 'مشکلی پیش آمده است.') => {
    swal.fire('خطا', desc, 'error');
};
const swalFireSuccess = (desc = 'با موفقیت انجام شد.') => {
    swal.fire('انجام شد!', desc, 'success');
};
const toastrFireError = (desc = 'مشکلی پیش آمده است.') => {
    toastr.error(desc);
};
const toastrFireSuccess = (desc = 'با موفقیت انجام شد.') => {
    toastr.success('انجام شد!', desc, 'success');
};
$('form').on("submit", function (e) {
    $(this).find('button[type=submit]').addClass('spinner spinner-white spinner-left');
    // $('form').find('input,select,textarea,button').addClass('disabled').prop('readonly', true);
});
const spinnerButtonON = (qs) => {
    if (qs.type === 'checkbox') {
        qs.parentElement.classList.add('opacity-30')
        $(qs).parent().parent().addClass('spinner spinner-dark spinner-left')
        qs.disabled = true;
    } else
        $(qs).addClass('spinner spinner-white spinner-left').prop("disabled", true)
};
const spinnerButtonOFF = (qs) => {
    if (qs.type === 'checkbox') {
        qs.parentElement.classList.remove('opacity-30')
        $(qs).parent().parent().removeClass('spinner spinner-dark spinner-left')
        qs.disabled = false;
    } else
        $(qs).removeClass('spinner spinner-white spinner-left disabled').prop("disabled", false)
};
$('form a').click(function (e) {
    if (!$(this).attr("href").startsWith('#'))
        $(this).addClass('spinner spinner-white spinner-left');
});
$('input.only-number').keydown(function (e) {
    $(this).val($(this).val().replace(/[^\d].+/, ""));
    if (!((e.which >= 48 && e.which <= 57) ||
        (e.which >= 96 && e.which <= 105) ||
        e.which === 16 ||
        e.which === 37 ||
        e.which === 35 ||
        e.which === 36 ||
        e.which === 39 ||
        e.which === 13 ||
        e.which === 17 ||
        e.which === 18 ||
        e.which === 27 ||
        e.which === 8 ||
        e.which === 9
    ))
        if (!((e.which > 48 && e.which < 57) || (e.which > 95 && e.which < 106)))
            e.preventDefault();
});


const code_meli_valid = (input) => {
    input = toEnglishDigit(input);
    if (!/^\d{10}$/.test(input)
        || input == '0000000000'
        || input == '1111111111'
        || input == '2222222222'
        || input == '3333333333'
        || input == '4444444444'
        || input == '5555555555'
        || input == '6666666666'
        || input == '7777777777'
        || input == '8888888888'
        || input == '9999999999')
        return false;
    var check = parseInt(input[9]);
    var sum = 0;
    var i;
    for (i = 0; i < 9; ++i) {
        sum += parseInt(input[i]) * (10 - i);
    }
    sum %= 11;
    return (sum < 2 && check == sum) || (sum >= 2 && check + sum == 11);
}

$('input.no-space').keydown(function (e) {
    $(this).val($(this).val().replace(/\s/g, ''))
});

const loadingFormENABLE = (querySelector = 'form', buttons = [], relative = false, size = null) => {
    if (document.querySelector(querySelector)) {
        document.querySelector(querySelector).parentElement.classList.add('form-loading');
        if (size)
            document.querySelector(querySelector).parentElement.classList.add('loading-sm');
        if (relative)
            document.querySelector(querySelector).parentElement.classList.add('position-relative');
        for (const btn of buttons)
            document.querySelector(btn).disabled = true
    }
};
const loadingFormDISABLE = (querySelector = 'form', buttons = [], relative = false) => {
    if (document.querySelector(querySelector)) {

        document.querySelector(querySelector).parentElement.classList.remove("form-loading");
        document.querySelector(querySelector).parentElement.classList.remove('loading-sm');
        for (const btn of buttons)
            document.querySelector(btn).disabled = false
    }
};
JalaliDate = {
    g_days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    j_days_in_month: [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
};

JalaliDate.jalaliToGregorian = function (j_y, j_m, j_d) {
    j_y = parseInt(j_y);
    j_m = parseInt(j_m);
    j_d = parseInt(j_d);
    var jy = j_y - 979;
    var jm = j_m - 1;
    var jd = j_d - 1;

    var j_day_no = 365 * jy + parseInt(jy / 33) * 8 + parseInt((jy % 33 + 3) / 4);
    for (var i = 0; i < jm; ++i) j_day_no += JalaliDate.j_days_in_month[i];

    j_day_no += jd;

    var g_day_no = j_day_no + 79;

    var gy = 1600 + 400 * parseInt(g_day_no / 146097); /* 146097 = 365*400 + 400/4 - 400/100 + 400/400 */
    g_day_no = g_day_no % 146097;

    var leap = true;
    if (g_day_no >= 36525) /* 36525 = 365*100 + 100/4 */
    {
        g_day_no--;
        gy += 100 * parseInt(g_day_no / 36524); /* 36524 = 365*100 + 100/4 - 100/100 */
        g_day_no = g_day_no % 36524;

        if (g_day_no >= 365) g_day_no++;
        else leap = false;
    }

    gy += 4 * parseInt(g_day_no / 1461); /* 1461 = 365*4 + 4/4 */
    g_day_no %= 1461;

    if (g_day_no >= 366) {
        leap = false;

        g_day_no--;
        gy += parseInt(g_day_no / 365);
        g_day_no = g_day_no % 365;
    }

    for (var i = 0; g_day_no >= JalaliDate.g_days_in_month[i] + (i == 1 && leap); i++)
        g_day_no -= JalaliDate.g_days_in_month[i] + (i == 1 && leap);
    var gm = i + 1;
    var gd = g_day_no + 1;

    gm = gm < 10 ? "0" + gm : gm;
    gd = gd < 10 ? "0" + gd : gd;

    return [gy, gm, gd];
}
$(document).keypress(
    function (event) {
        if (event.which === 13) {
            event.preventDefault();
        }
    });
$('input').keypress(function (event) {
    if (event.which === 13) {
        const parentForm = $(this).parents('form:first');
        for (const button of parentForm.find('button.btn-primary')) {
            if ($(button).css('display') !== 'none') {
                $(button).click();
            }
        }
        event.preventDefault();
        $(this).closest('button.btn-primary').click();
    }
});
const formatNumber = (n) => {
    // format number 1000000 to 1,234,567
    return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

const deFormatNumber = (n) => {
    // format number 1000000 to 1,234,567
    let res = n.replace(/\D/g, "").replace(",", "")
    if (res === '')
        return '0'
    return res
}

const formatCurrency = (input, blur) => {
    // appends $ to value, validates decimal side
    // and puts cursor back in right position.

    // get input value
    let input_val = input.val();

    if (input_val === '') {
        return;
    }
    let original_len = input_val.length;

    let caret_pos = input.prop("selectionStart");
    if (input_val.indexOf(".") >= 0) {
        var decimal_pos = input_val.indexOf(".");
        var left_side = input_val.substring(0, decimal_pos);
        var right_side = input_val.substring(decimal_pos);
        left_side = formatNumber(left_side);
        right_side = formatNumber(right_side);
        right_side = right_side.substring(0, 2);
        input_val = left_side + " ریال";

    } else {
        input_val = formatNumber(input_val);
        input_val = input_val + " ریال";
        input.val(input_val);
        let updated_len = input_val.length;
        caret_pos = updated_len - original_len + caret_pos;
        input[0].setSelectionRange(caret_pos, caret_pos);
    }
}

$(".currency").on({
    keyup: () => {
        formatCurrency($(this));
    },
    blur: () => {
        formatCurrency($(this), "blur");
    }
});
for (const input of document.querySelectorAll('.currency')) {
    formatCurrency($(input));
}

const toEnglishDate = (value) => {
    if (value.length > 5) {
        let dateSplit = toEnglishDigit(value).split("/"),
            jD = JalaliDate.jalaliToGregorian(dateSplit[0], dateSplit[1], dateSplit[2])
        return jD[0] + "-" + jD[1] + "-" + jD[2];
    } else {
        return null;
    }
};
const date_picker_config = {
    altFormat: 'X',
    calendarType: 'persian',
    initialValueType: 'gregorian',
    persianDigit: false,
    format: 'YYYY/MM/D',
    observer: true,
    initialValue: true,
    timePicker: {
        enabled: false
    },
    toolbox: {
        calendarSwitch: {
            enabled: false
        }
    },
};
if (document.querySelector('.date'))
    $('.date').persianDatepicker(date_picker_config);

const ScrollToElement = (qs, where = null, offset = 0) => {
    if (!where)
        where = qs
    document.querySelector(qs).scrollTop = document.querySelector(where).scrollHeight + offset;
}

function isScrolledIntoView(elem) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

function Utils() {

}

Utils.prototype = {
    constructor: Utils,
    isElementInView: function (element, fullyInView) {
        var pageTop = $(window).scrollTop();
        var pageBottom = pageTop + $(window).height();
        var elementTop = $(element).offset().top;
        var elementBottom = elementTop + $(element).height();

        if (fullyInView === true) {
            return ((pageTop < elementTop) && (pageBottom > elementBottom));
        } else {
            return ((elementTop <= pageBottom) && (elementBottom >= pageTop));
        }
    }
};

var Utils = new Utils();


const CurrentUrl = location.pathname;
const urlHref = $(`.menu-nav a[href="${CurrentUrl}"]`)
if (CurrentUrl === "/")
    document.querySelector('#kt_header_menu a').parentElement.classList.add("menu-item-active")
else if (urlHref.length) {
    urlHref.parent().addClass("menu-item-active")
    urlHref.parent().parent().parent().parent().addClass("menu-item-active")
}
if (document.querySelector('.menu-item-active > a > .menu-text')) {
    if (document.getElementById('id_module')) {
        document.getElementById('id_module').innerHTML = document.querySelector('.menu-item-active > a > .menu-text').innerHTML
        document.getElementById('id_module').parentElement.classList.remove('d-none')
    }
}

const tableToExcel = (function () {
    let uri = 'data:application/vnd.ms-excel;base64,'
        ,
        template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/><x:DisplayRightToLeft/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        }
        , format = function (s, c) {
            return s.replace(/{(\w+)}/g, function (m, p) {
                return c[p];
            })
        }
    return function (table, name, filename) {
        if (!table.nodeType) table = document.getElementById(table)
        let ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
        window.open(uri + base64(format(template, ctx)));
    }
})();

const regexFA = /^[پچجحخهعغفقثصضشسیبلاتنمآکگوئدذرزطظژؤإأءًٌٍَُِّ\s\n\r\t\d\(\)\[\]\{\}.,،;\-؛]+$/;