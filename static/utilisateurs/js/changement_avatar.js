function recuperer_avatar() {
    $.ajax({
        url: 'utilisateurs/recuperer_avatar.php',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            $('#avatar').attr('src', data.avatar);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function recuperer_etat_page_django_avatar() {
    let contenu_page = '';
    $.ajax({
        url: '/avatar/change',
        type: 'GET',
        dataType: 'html',
        success: function (data) {
            contenu_page = data;
            console.log(contenu_page);
        }
    });
}

$(document).ready(function () {
    recuperer_etat_page_django_avatar();
});
