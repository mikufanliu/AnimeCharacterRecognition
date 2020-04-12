let preview = document.querySelector('#preview');
let eleFile = document.getElementById('upload_input');
eleFile.addEventListener('change', function () {
    let file = this.files[0];
    console.log("Input change")
    // 确认选择的文件是图片
    if (file.type.indexOf("image") == 0) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            // 图片base64化
            let newUrl = this.result;
            preview.src = newUrl;
        };
    }

    document.getElementById('name').style.display = "none";
});

$(document).ready(function(){
    $('#up').click(function(){
        $('#upload_input').click();
    });

});
