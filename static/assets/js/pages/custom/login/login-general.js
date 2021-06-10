const TOKEN_LOGIN = '/api/v1/token/';
const REGISTER_URL = '/api/v1/signup/';
localStorage.removeItem('session_key');
localStorage.removeItem('session_refresh');
"use strict";

// Class Definition
var KTLogin = function () {
    var _login;

    var _showForm = function (form) {
        var cls = 'login-' + form + '-on';
        var form = 'kt_login_' + form + '_form';

        _login.removeClass('login-forgot-on');
        _login.removeClass('login-signin-on');
        _login.removeClass('login-signup-on');

        _login.addClass(cls);

        KTUtil.animateClass(KTUtil.getById(form), 'animate__animated animate__backInUp');
    }

    var _handleSignInForm = function () {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_signin_form'),
            {
                fields: {
                    username: {
                        validators: {
                            notEmpty: {
                                message: 'پر کردن فیلد نام کاربری اجباری است!'
                            }
                        }
                    },
                    password: {
                        validators: {
                            notEmpty: {
                                message: 'پر کردن فیلد رمز عبور اجباری است!'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    submitButton: new FormValidation.plugins.SubmitButton(),
                    //defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signin_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                if (status === 'Valid') {
                    document.getElementById('kt_login_signin_submit').className = 'spinner pl-15 spinner-track spinner-dark spinner-left btn btn-primary font-weight-bolder font-size-h6 px-8 py-4 my-3 mr-3'
                    $.ajax({
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'POST',
                        url: TOKEN_LOGIN,
                        data: JSON.stringify({
                            username: document.querySelector('#kt_login_signin_form input[name=username]').value,
                            password: document.querySelector('#kt_login_signin_form input[name=password]').value,
                        }),
                        success: function (res) {
                            console.log(res)
                            localStorage.setItem('session_key', 'Bearer ' + res["access"]);
                            localStorage.setItem('session_refresh', res["refresh"]);
                            document.getElementById('kt_login_signin_form').submit()
                        },
                        error: function (res) {
                            console.log(res)
                            if (res['status'] === 401) {
                                swalFireError('نام کاربری و رمز عبور وارد شده صحیح نمی باشد!');
                                document.getElementById('kt_login_signin_submit').className = 'btn btn-primary font-weight-bolder font-size-h6 px-8 py-4 my-3 mr-3'

                            } else {
                                swalFireError('مشکلی پیش آمده است لطفا دوباره امتحان کنید!');
                                document.getElementById('kt_login_signin_submit').className = 'btn btn-primary font-weight-bolder font-size-h6 px-8 py-4 my-3 mr-3'

                            }
                        }
                    });
                } else {

                    swal.fire({
                        text: "تعدادی خطا جهت ورود وجود دارد! لطفا دوباره تلاش کنید!",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "متوجه شدم!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

        // Handle forgot button
        $('#kt_login_forgot').on('click', function (e) {
            e.preventDefault();
            _showForm('forgot');
        });

        // Handle signup
        $('#kt_login_signup').on('click', function (e) {
            e.preventDefault();
            _showForm('signup');
        });
    }
    var _handleSignUpForm = function (e) {
        var validation;
        var form = KTUtil.getById('kt_login_signup_form');

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            form,
            {
                fields: {
                    username: {
                        validators: {
                            callback: {
                                message: 'نام کاربری باید فقط شامل حروف و اعداد انگلیسی باشد!',
                                callback: function (input) {
                                    if (input.value.length)
                                        return /^[a-zA-Z0-9_.-]+$/.test(input.value);
                                    else
                                        return true
                                }
                            },
                            notEmpty: {
                                message: 'پر کردن فیلد نام کاربری اجباری است!'
                            }
                        }
                    },
                    first_name: {
                        validators: {
                            notEmpty: {
                                message: 'پر کردن فیلد نام اجباری است!'
                            },
                            regexp: {
                                regexp: regexFA,
                                message: 'فقط حروف فارسی وارد شود!'
                            },
                        }
                    },
                    last_name: {
                        validators: {
                            notEmpty: {
                                message: 'پر کردن فیلد نام خانوادگی اجباری است!'
                            },
                            regexp: {
                                regexp: regexFA,
                                message: 'فقط حروف فارسی وارد شود!'
                            },
                        }
                    },
                    // email: {
                    //     validators: {
                    //         notEmpty: {
                    //             message: 'پر کردن فیلد ایمیل اجباری است!'
                    //         },
                    //         emailAddress: {
                    //             message: 'ایمیل وارد شده معتبر نیست!'
                    //         }
                    //     }
                    // },
                    password: {
                        validators: {
                            stringLength: {
                                min: 6,
                                max: 50,
                                message:
                                    'رمز عبور باید حداقل 6 حرفی باشد!'
                            },
                            notEmpty: {
                                message: 'پر کردن فیلد رمز عبور اجباری است!'
                            }
                        }
                    },
                    repeat_password: {
                        validators: {
                            notEmpty: {
                                message: 'تایید رمز عبور الزامی می باشد!'
                            },
                            identical: {
                                compare: function () {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'رمز عبور و تکرار رمز عبور باید یکسان باشند!'
                            }
                        }
                    },
                    mobile_number: {
                        validators: {
                            stringLength: {
                                min: 11,
                                max: 11,
                                message: 'شماره تماس باید 11 رقمی باشد!'
                            },
                            integer: {
                                message: 'شماره تماس باید فقط عدد وارد شود',
                            },
                            notEmpty: {
                                message: 'وارد کردن شماره تلفن ضروری است'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signup_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                    if (status === 'Valid') {

                        ApiAjax({
                            method: 'POST',
                            url: REGISTER_URL,
                            token: false,
                            success_url: '/',
                            button: document.getElementById('kt_login_signin_submit'),
                            form: '#kt_login_signup_form',
                            success: function (res) {
                                localStorage.setItem('session_key', 'Bearer ' + res["access"]);
                                localStorage.setItem('session_refresh', res["refresh"]);
                            }
                        })
                    } else {
                        swal.fire({
                            text: "تعدادی خطا جهت ثبت نام وجود دارد! لطفا دوباره تلاش کنید!",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "متوجه شدم!",
                            customClass: {
                                confirmButton: "btn font-weight-bold btn-light-primary"
                            }
                        }).then(function () {
                            KTUtil.scrollTop();
                        });
                    }
                }
            );
        });

        // Handle cancel button
        $('#kt_login_signup_cancel').on('click', function (e) {
            e.preventDefault();

            _showForm('signin');
        });
    }

    var _handleForgotForm = function (e) {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_forgot_form'),
            {
                fields: {
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'پر کردن فیلد ایمیل اجباری است!'
                            },
                            emailAddress: {
                                message: 'ایمیل وارد شده معتبر نیست!'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        // Handle submit button
        $('#kt_login_forgot_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                if (status == 'Valid') {
                    // Submit form
                    document.getElementById('kt_login_forgot_submit').className = 'btn btn-primary font-weight-bolder font-size-h6 px-8 py-4 my-3 mr-4 spinner pl-15 spinner-track spinner-dark spinner-left';
                    document.getElementById('kt_login_forgot_form').submit();
                } else {
                    swal.fire({
                        text: "تعدادی خطا برای ثبت نام وجود دارد! لطفا دوباره تلاش کنید!",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "متوجه شدم!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

        // Handle cancel button
        $('#kt_login_forgot_cancel').on('click', function (e) {
            e.preventDefault();

            _showForm('signin');
        });
    }

    // Public Functions
    return {
        // public functions
        init: function () {
            _login = $('#kt_login');

            _handleSignInForm();
            _handleSignUpForm();
            _handleForgotForm();
        }
    };
}();

// Class Initialization
