window.data_table_cool_options = {
    columnDefs: [
        {className: "text-center", targets: "_all"},
    ],
    "aaSorting": [],
    'paging': true,
    'lengthChange': true,
    'searching': true,
    'ordering': true,
    'info': true,
    'autoWidth': true,
    'responsive': false,
    'oLanguage': {
        "sSearch": "جستجو: ",
        "sLengthMenu": "تعداد در صفحه: _MENU_ ",
        "sInfo": "نمایش _START_ تا _END_ از _TOTAL_ مورد",
        "oPaginate": {
            "sFirst": "صفحه اول", // This is the link to the first page
            "sPrevious": "قبلی", // This is the link to the previous page
            "sNext": "بعدی", // This is the link to the next page
            "sLast": "صفحه آخر", // This is the link to the last page
        },
        "sEmptyTable": "اطلاعاتی در جدول شما ثبت نشده است.",
        "sInfoEmpty": "اطلاعات یافت نشد.",
        "sZeroRecords": "اطلاعاتی برای نمایش وجود ندارد.",
        "sInfoFiltered": " - فیلتر اطلاعات از  _MAX_ رکورد",
        sProcessing: ''
    }
};
var raw_data_table_cool_options = JSON.parse(JSON.stringify(window.data_table_cool_options));
window.getData = function (oTable, ele) {
    return oTable.row(ele.closest('tr')).data()
};
window.getId = function (oTable, ele) {
    return getData(oTable, ele)[0]
};

window.datatable_simple_show = function (options, settings) {
    if (!settings)
        settings = {};
    var window_options = $.extend(true, {}, window.data_table_cool_options, settings);
    window_options["processing"] = true;
    window_options["serverSide"] = true;
    // url which we get table's data from
    if (options['extra_filters']) {
        window_options["ajax"] = {
            url: options['url'],
            method: 'POST',
            'beforeSend': (request) => request.setRequestHeader("Authorization", localStorage.getItem('session_key')),
            data: function (d) {
                options['extra_filters'](d);
                // console.log(d);
            },
        };
        if (!options['no_error']) {
            window_options["ajax"]['error'] = function (xhr, error, code) {
                checkToken(xhr, (tokenStatus) => {
                    if (tokenStatus === true) {
                        oTable.draw(false);
                    } else {
                        console.error('UNKNOWN ERROR Backend RES :', xhr);
                        console.log('tokenStatus:', tokenStatus)
                    }
                });
            }
        }
    } else
        window_options["ajax"] = options['url'];
    // add a column to overall columns so we can have delete and edit buttons
    window_options["columns"] = [];
    do_not_order = options["do_not_order"] ? options["do_not_order"] : [];
    for (var i = 0; i < options['real_cols']; i++) {
        defaulta = {
            className: "text-center",
        };
        if (options['this_column_data']) {
            options['this_column_data'](i, defaulta);
        }
        if (do_not_order.includes(i)) {
            defaulta['orderable'] = false;
        }
        window_options["columns"].push(defaulta);
    }
    extra_buttons = options["ex_buttons"] ? options["ex_buttons"] : "";
    delete_text = options['delete_text'] ? options['delete_text'] : "حذف";
    edit_text = options['edit_text'] ? options['edit_text'] : "ویرایش";
    if (!options["no_action_nutton"]) {
        buttons = '';
        if (options["extras"]) {
            buttons += `<div class="dropdown dropdown-inline"><a href="javascript:;" class="btn btn-sm btn-light-primary btn-text-primary btn-icon mr-2 setID" data-toggle="dropdown"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1" class="svg-icon"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M7,3 L17,3 C19.209139,3 21,4.790861 21,7 C21,9.209139 19.209139,11 17,11 L7,11 C4.790861,11 3,9.209139 3,7 C3,4.790861 4.790861,3 7,3 Z M7,9 C8.1045695,9 9,8.1045695 9,7 C9,5.8954305 8.1045695,5 7,5 C5.8954305,5 5,5.8954305 5,7 C5,8.1045695 5.8954305,9 7,9 Z" fill="#000000"></path><path d="M7,13 L17,13 C19.209139,13 21,14.790861 21,17 C21,19.209139 19.209139,21 17,21 L7,21 C4.790861,21 3,19.209139 3,17 C3,14.790861 4.790861,13 7,13 Z M17,19 C18.1045695,19 19,18.1045695 19,17 C19,15.8954305 18.1045695,15 17,15 C15.8954305,15 15,15.8954305 15,17 C15,18.1045695 15.8954305,19 17,19 Z" fill="#000000" opacity="0.3"></path></g></svg></span></a>
            <div class="dropdown-menu nowrap-text dropdown-menu-sm dropdown-menu-right"><ul class="navi flex-column navi-hover py-2"><li class="navi-header text-uppercase font-size-x text-primary pb-2">عملیات را انتخاب کنید:</li>${options['extras'].join('')}</ul></div></div>`
        }
        if (options["icon_edit"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="ویرایش" class="btn btn-sm btn-light-primary ml-2 edit_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M12.2674799,18.2323597 L12.0084872,5.45852451 C12.0004303,5.06114792 12.1504154,4.6768183 12.4255037,4.38993949 L15.0030167,1.70195304 L17.5910752,4.40093695 C17.8599071,4.6812911 18.0095067,5.05499603 18.0083938,5.44341307 L17.9718262,18.2062508 C17.9694575,19.0329966 17.2985816,19.701953 16.4718324,19.701953 L13.7671717,19.701953 C12.9505952,19.701953 12.2840328,19.0487684 12.2674799,18.2323597 Z" fill="#000000" fill-rule="nonzero" transform="translate(14.701953, 10.701953) rotate(-135.000000) translate(-14.701953, -10.701953) "></path><path d="M12.9,2 C13.4522847,2 13.9,2.44771525 13.9,3 C13.9,3.55228475 13.4522847,4 12.9,4 L6,4 C4.8954305,4 4,4.8954305 4,6 L4,18 C4,19.1045695 4.8954305,20 6,20 L18,20 C19.1045695,20 20,19.1045695 20,18 L20,13 C20,12.4477153 20.4477153,12 21,12 C21.5522847,12 22,12.4477153 22,13 L22,18 C22,20.209139 20.209139,22 18,22 L6,22 C3.790861,22 2,20.209139 2,18 L2,6 C2,3.790861 3.790861,2 6,2 L12.9,2 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"></path></g></svg></span></button> ';
        } else if (!options["not_edit_able"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="ویرایش" class="btn btn-sm btn-light-primary btn-icon ml-2 edit_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M12.2674799,18.2323597 L12.0084872,5.45852451 C12.0004303,5.06114792 12.1504154,4.6768183 12.4255037,4.38993949 L15.0030167,1.70195304 L17.5910752,4.40093695 C17.8599071,4.6812911 18.0095067,5.05499603 18.0083938,5.44341307 L17.9718262,18.2062508 C17.9694575,19.0329966 17.2985816,19.701953 16.4718324,19.701953 L13.7671717,19.701953 C12.9505952,19.701953 12.2840328,19.0487684 12.2674799,18.2323597 Z" fill="#000000" fill-rule="nonzero" transform="translate(14.701953, 10.701953) rotate(-135.000000) translate(-14.701953, -10.701953) "></path><path d="M12.9,2 C13.4522847,2 13.9,2.44771525 13.9,3 C13.9,3.55228475 13.4522847,4 12.9,4 L6,4 C4.8954305,4 4,4.8954305 4,6 L4,18 C4,19.1045695 4.8954305,20 6,20 L18,20 C19.1045695,20 20,19.1045695 20,18 L20,13 C20,12.4477153 20.4477153,12 21,12 C21.5522847,12 22,12.4477153 22,13 L22,18 C22,20.209139 20.209139,22 18,22 L6,22 C3.790861,22 2,20.209139 2,18 L2,6 C2,3.790861 3.790861,2 6,2 L12.9,2 Z" fill="#000000" fill-rule="nonzero" opacity="0.3"></path></g></svg></span></button>';
        }
        if (options["icon_delete"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="حذف" class="btn btn-sm btn-light-primary delete_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"></path><path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"></path></g></svg></span></button> ';

        } else if (!options["not_delete_able"]) {
            buttons += '<button type="button" data-skin="dark" data-toggle="tooltip" data-placement="top" title="" data-original-title="حذف"  class="btn btn-sm btn-light-primary btn-icon delete_button"><span class="svg-icon svg-icon-md"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24px" height="24px" viewBox="0 0 24 24" version="1.1"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><rect x="0" y="0" width="24" height="24"></rect><path d="M6,8 L6,20.5 C6,21.3284271 6.67157288,22 7.5,22 L16.5,22 C17.3284271,22 18,21.3284271 18,20.5 L18,8 L6,8 Z" fill="#000000" fill-rule="nonzero"></path><path d="M14,4.5 L14,4 C14,3.44771525 13.5522847,3 13,3 L11,3 C10.4477153,3 10,3.44771525 10,4 L10,4.5 L5.5,4.5 C5.22385763,4.5 5,4.72385763 5,5 L5,5.5 C5,5.77614237 5.22385763,6 5.5,6 L18.5,6 C18.7761424,6 19,5.77614237 19,5.5 L19,5 C19,4.72385763 18.7761424,4.5 18.5,4.5 L14,4.5 Z" fill="#000000" opacity="0.3"></path></g></svg></span></button>';
        }
        window_options["columns"].push(
            {
                data: null,
                className: "text-center",
                orderable: false,
                defaultContent: extra_buttons + buttons
            });

        if (!options["no_loading"]) {
            $(options['datable_id']).parent().prepend(`<div class="loading-1-container loading-1-custom"><div class="loading-1"><div></div><div></div><div><div></div></div><div><div></div></div></div></div>`)
        }
    }
    $(document).ready(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
    // hide id columnRadeNezami
    if (!window_options["columnDefs"])
        window_options["columnDefs"] = [];

    if (options['hide_id']) {
        window_options["columnDefs"].push({
            "targets": [0],
            "visible": false,
            "searchable": false
        });
    }
    if (options['responsive']) {
    }
    // window.data_table_cool_options["scrollX"] = true;
    // window.data_table_cool_options["responsive"] = true;
    // create datatable
    var oTable = $(options['datable_id']).DataTable(window_options);
    // a returns id of a column
    if (!options["no_action_nutton"]) {
        if (!options["not_edit_able"]) {
            // parse urls for deleting and editing
            var update_url = options['up_url'];


            update_url = update_url.substr(0, update_url.length - 1);
        }
        var delete_url = options['del_url'];
        delete_url = delete_url.substr(0, delete_url.length - 1);
    }
    // on redraw re listen to delete and edit buttons
    oTable.on('draw.dt', function () {
        // edit button
        if (!options["no_loading"]) {
            loadingFormDISABLE(`.loading-1-custom`, [], true)
        }
        $(options['datable_id'] + " " + '.edit_button').on('click', function (e) {

            if (!options["no_loading"]) {
                loadingFormENABLE(`.loading-1-custom`, [], true)
            }
            e.preventDefault();

            var id = getId(oTable, $(this));
            window.location.href = update_url + id;
        });
        // delete button
        if (options['do_before_initializing']) {
            options['do_before_initializing'](oTable);
        }
        $('.dataTables_filter').parent().parent().addClass('modal-header').css({
            "margin-left": "0px",
            "margin-right": "0px"
        });
        $('.dataTables_filter input').parent().parent().parent().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6')
            .siblings().removeClass('col-sm-6').addClass('col-sm-12 col-lg-6');
        $(options['datable_id'] + " " + '.delete_button').on('click', function (e) {
            e.preventDefault();
            var id = getId(oTable, $(this));
            var deleting_process = function (callback) {
                if (options['extra_del_params']) {
                    if (options['extra_del_params']['ajax']) {
                        $.ajax(delete_url + id, {
                            method: 'delete',
                            headers: {
                                "Authorization": localStorage.getItem('session_key')
                            },
                            error: (options['deleteError']) ? options['deleteError'] : (error) => {
                                let errorMessage = ''
                                console.log(error)
                                if (error.responseText && error.status === 500)
                                    errorMessage = 'موارد استفاده شده:' + '<br>' + error.responseText
                                if (error.responseJSON && error.status === 400) {
                                    for (const key in error.responseJSON) {
                                        console.log(key)
                                        console.log(error.responseJSON)
                                        if (error.responseJSON[key] instanceof Array) {
                                            errorMessage += error.responseJSON[key].join(' <br> ')
                                        }
                                    }
                                }
                                swalFireError('قابل حذف نمی باشد!' + '<br>' + errorMessage)
                            }
                        }).done(function (res) {
                            oTable.draw();
                            if (callback) callback();
                        });
                        return
                    }
                }
                if (callback) callback();
                window.location.href = delete_url + id;
            };
            if (options["modal_id"]) {
                $(options["modal_id"]).modal('show');
                $(options['modal_id'] + " " + '.yes_button').click(function () {
                    $(options["modal_id"]).modal('toggle');
                    deleting_process()
                });
            } else {
                swal.fire({
                    title: 'آیا مطمئن هستید ؟',
                    text: "رکورد پس از حذف قابل بازگشت نخواهد بود !",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'بله! حذفش کن',
                    cancelButtonText: 'لغو',

                }).then(function (result) {
                    if (result.value) {
                        deleting_process(function () {
                            toastr.success('رکورد مورد نظر با موفقیت حذف شد.')
                        });
                    }
                });
            }
        });
        $(options['datable_id'] + " " + '.load-form').on('click', function (e) {
            e.preventDefault();
            if (options["no_loading"]) {
                $(options['datable_id']).parent().prepend(`<div class="loading-1-container loading-1-custom"><div class="loading-1"><div></div><div></div><div><div></div></div><div><div></div></div></div></div>`)
            }
            loadingFormENABLE(`.loading-1-custom`, [], true)
        });
        if (options['loading_all'])
            $(options['datable_id'] + " " + '.btn:not(.delete_button)').on('click', function (e) {
                if (!document.querySelector('.loading-1-custom')) {
                    $(options['datable_id']).parent().prepend(`<div class="loading-1-container loading-1-custom"><div class="loading-1"><div></div><div></div><div><div></div></div><div><div></div></div></div></div>`)
                }
                loadingFormENABLE(`.loading-1-custom`, [], true)
            });

    });

    var timer = null;
    var last_input = null;

    function searcher(type) {
        return function (e) {
            clearTimeout(timer);
            if (last_input !== e.target.value) {
                if (!type)
                    setTimeout(function () {
                        oTable.search(e.target.value);
                        oTable.draw();
                    }, 800);
                else {
                    setTimeout(function () {
                        oTable.search(e.target.value);
                        oTable.draw();
                    }, 35);
                }
            }
        };
    };
    $(options['datable_id'] + '_wrapper input[type="search"]').off().on('keyup', searcher(false))
        .on('click', searcher(true));
    if (options['after_init']) {
        options['after_init'](oTable, options);
    }
    return $.extend(oTable, {
        getId: function (e) {
            return window.getId(oTable, e)
        },
        getData: function (e) {
            return window.getData(oTable, e)
        }
    });
};
var allText = {}

function minimizeText(row, data, id, query = id - 1, sub = 27) {
    if (data[id].length > sub + 3) {
        if (!allText[query]) {
            allText[query] = {}
        }
        allText[query][data[0]] = data[id];
        var tdEq = 'td:eq(' + query + ')';
        return $(tdEq, row).html('<span type="button" onclick="showTextMini(' + data[0] + ',' + query + ')" class="text-center">' + data[id].substring(0, sub) + '...' + '</span>')
    } else return null
}


function showTextMini(id, query) {
    swal.fire({
        title: "متن کامل:",
        html: '<pre style="white-space: pre-wrap;' +
            'white-space: -moz-pre-wrap;' +
            'white-space: -pre-wrap;' +
            'white-space: -o-pre-wrap;' +
            'word-wrap: break-word;">' + allText[query][id] + '</pre>',
        confirmButtonText: 'بستن',
        width: 'auto',
    });
    $('.swal2-popup').css('min-width', '400px')
}

const naviItem = (text = '', icon = '', extraClass = '', href = '#') => {
    return `<li class="navi-item"><a href="${href}" class="navi-link ${extraClass}"><span class="navi-icon"><i class="${icon}"></i></span><span class="navi-text">${text}</span></a></li>`
};

const boldCol = (query, row, data) => {
    let arg = 'td:eq(' + query + ')';
    if (isNaN(data[0]) && data[0]) data = data[0].toUpperCase() + data.slice(1);
    return $(arg, row).html(`<div class="font-weight-bolder text-primary mb-0"> ${data}</div>`);
};
const bolderCol = (query, row, data) => {
    let arg = 'td:eq(' + query + ')';
    return $(arg, row).html(`<div class="font-weight-bolder mb-0"> ${data}</div>`);
};
