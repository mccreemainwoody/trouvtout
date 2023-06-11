$(document).ready(function () {
    $('.form-ajout-fichier').change(function (event) {
        event.preventDefault();

        let csrf_token = $('input[name="csrfmiddlewaretoken"]').attr('value');
        let id_trouv = $(this).siblings('input[name="trouv"]').attr('value');
        let fichier = $(this).prop('files')[0];
        let form_data = new FormData();
        form_data.append('csrfmiddlewaretoken', csrf_token);
        form_data.append('id_trouv', id_trouv);
        form_data.append('fichier', fichier);

        $.ajax({
            url: '/api/trouvs/ajout-fichier-trouv',
            type: 'POST',
            data: form_data,
            contentType: false,
            processData: false,
            success: function () {
                $('.liste-fichiers-trouv').append(
                    '<li aria-id-fichier="' + id_trouv + '">' +
                        '<a href="#" class="bouton-suppression-fichier"><i class="fas fa-trash-alt" aria-hidden="true"></i></a>' +
                        '<a href="#" class="bouton-suppression-fichier">fichiers/' + fichier.name + '</a>' +
                    '</li>');
            },
            error: (content) => $(this).parent().parent().add(content.responseText),
            complete: () =>  $(this).val('')
        });
    });
    //...

    $('.bouton-suppression-fichier').click(function (event) {
        event.preventDefault();

        let ligne_fichier = $(this).parent();
        let id_fichier = ligne_fichier.attr('aria-id-fichier');
        let id_trouv = $(this).closest('ul').siblings('input[name="id"]').attr('value');

        $.ajax({
            url: '/api/trouvs/suppression-fichier-trouv?id_trouv=' + id_trouv + '&id_fichier=' + id_fichier,
            type: 'GET',
            success: () => ligne_fichier.fadeOut(500),
            error: () => ligne_fichier.children().add('<p>Erreur lors de la suppression du fichier !</p>')
        });
    });
})