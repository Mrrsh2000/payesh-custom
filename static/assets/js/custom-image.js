const imageFieldSelector = ".image-field-1 > .d-none input";
const imageField = document.querySelector(imageFieldSelector)
const imageBackGround = document.getElementById('image_field').src
$('.image-field-hover').click(function () {
    if (imageField.files.length == 0) {
        imageField.click();
    } else {
        var myId = '#image_field';
        imageField.value = "";
        $(myId).attr('src', imageBackGround);
        document.querySelector('.image-field-hover div').innerHTML = '<i class="fa fa-upload large"></i>'
    }
})

$(imageFieldSelector).change(function () {

    var control = imageField;
    var files = control.files;
    var errorText = '';
    var errorIs = false;
    for (var i = 0; i < files.length; i++) {
        if (files[i].type.includes("jpeg") || files[i].type.includes("png")) {
            errorText = ''
        } else {
            errorText += 'فرمت فایل باید jpg/png باشد' + '<br>';
            errorIs = true;
        }
        if (files[i].size > 2621440) {
            errorText += 'حجم عکس نباید بیشتر از 2.5 مگابایت باشد' + '<br>';
            errorIs = true;
        }
        if (errorIs) {
            swal.fire({
                title: 'خطا',
                html: '<div class="swal2-html-container">' + errorText + '</div>',
                icon: "error",
                confirmButtonText: "متوجه شدم!",
                customClass: {
                    confirmButton: "btn font-weight-bold btn-secondary"
                }
            });
            $(imageFieldSelector).val('');
        }
    }
    readURL(this);
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var image = new Image();
            image.src = e.target.result;
            var myId = '#image_field';
            $(myId).attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]); // convert to base64 string

        document.querySelector('.image-field-hover div').innerHTML = '<i class="fa fa-trash large"></i>'
    }
}
