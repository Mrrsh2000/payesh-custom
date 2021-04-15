"use strict";

// Class definition
var KTWizard3 = function () {
	// Base elements
	var _wizardEl;
	var _formEl;
	var _wizard;
	var _validations = [];

	// Private functions
	var initWizard = function () {
		// Initialize form wizard
		_wizard = new KTWizard(_wizardEl, {
			startStep: 1, // initial active step number
			clickableSteps: true  // allow step clicking
		});

		// Validation before going to next page
		_wizard.on('beforeNext', function (wizard) {
			_validations[wizard.getStep() - 1].validate().then(function (status) {
				if (status == 'Valid') {
					_wizard.goNext();
					KTUtil.scrollTop();
				} else {
					Swal.fire({
						text: "لطفاً ابتدا خطا ها را برطرف کنید!",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "متوجه شدم",
						customClass: {
							confirmButton: "btn font-weight-bold btn-light"
						}
					}).then(function () {
						KTUtil.scrollTop();
					});
				}
			});

			_wizard.stop();  // Don't go to the next step
		});

		$('#submitter').click(function (e) {
                e.preventDefault();
                _validations[3].validate().then(function (status) {
                    if (status == 'Valid') {
                        ApiAjax({
                            success_url: '/',
                            url: EDIT_MY_LEGAL_PROFILE,
                            form: 'form',
                            method: 'PUT',
                            file: true,
                            button: document.getElementById('submitter'),
                            success_message: 'اطلاعات شما با موفقیت ویرایش شد!',
                        })
                    }
                });
            });

		// Change event
		_wizard.on('change', function (wizard) {
			KTUtil.scrollTop();
		});
	}

	var initValidation = function () {
		// Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
		// Step 1
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
					title: {
						validators: {
							notEmpty: {
								message: 'لطفا عنوان را وارد کنید!'
							}
						}
					},
					email: {
						validators: {
							notEmpty: {
								message: 'لطفا ایمیل را وارد کنید!'
							},
							emailAddress: {
								message: 'آدرس ایمیل صحیح نیست!'
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
						},
					},
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));

		// Step 2
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
					type: {
						validators: {
							notEmpty: {
								message: 'لطفا نوع سازمان را انتخاب کنید!'
							}
						}
					},
					website:{
						validators: {
							callback: {
								message: 'آدرس وبسایت وارد شده صحیح نمی باشد!',
								callback: function (input) {
									var english = /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g;
									return regexIfNotEmpty(input,english)
								}
							}
						}
					}
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));

		// Step 3
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
					state: {
						validators: {
							notEmpty: {
								message: 'لطفا استان را انتخاب کنید!'
							}
						}
					},
					city: {
						validators: {
							notEmpty: {
								message: 'لطفا شهر را انتخاب کنید!'
							}
						}
					},
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));

		// Step 4
		_validations.push(FormValidation.formValidation(
			_formEl,
			{
				fields: {
					interests: {
						validators: {
							notEmpty: {
								message: 'حداقل یک علاقه مندی ثبت کنید!'
							}
						}
					},
					work_area: {
						validators: {
							notEmpty: {
								message: 'حداقل یک علاقه مندی ثبت کنید!'
							}
						}
					},
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));
	}

	return {
		// public functions
		init: function () {
			_wizardEl = KTUtil.getById('kt_wizard_v3');
			_formEl = KTUtil.getById('kt_form');

			initWizard();
			initValidation();
		}
	};
}();

jQuery(document).ready(function () {
	KTWizard3.init();
});
