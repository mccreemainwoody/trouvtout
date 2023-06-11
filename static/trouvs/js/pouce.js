$(document).ready(function () {
    let messages_erreur = {
        404: 'Tiens donc, ce trouv ne semble pas vouloir recevoir votre réaction. Réessayez plus tard !',
        500: 'Oups, on dirait qu\'une erreur interne est survenue. Réessayez plus tard !'
    }
    messages_erreur[400] = messages_erreur[500]

    $('.pouce').click(function () {
        let pouce = $(this);
        let selecteur_trouv = pouce.closest('.trouv');
        let id_trouv = selecteur_trouv.attr('aria-id-trouv');
        let valeur = pouce.attr('value');
        let autre_pouce = pouce.siblings('[value='+-(valeur)+']');

        let bouton_affichage_total_trouv = selecteur_trouv.find('.affichage')
        let bloc_erreur = selecteur_trouv.find('.texte-erreur');
        let texte_erreur = bloc_erreur.find('p')

        if (pouce.hasClass('btn-success') || pouce.hasClass('btn-danger')) valeur = 0;

        $.ajax({
            url: 'http://127.0.0.1:8000/api/trouvs/pouce?trouv=' + id_trouv + '&valeur=' + valeur,
            type: 'GET',
            dataType: 'html',
            success: function (data) {
                bloc_erreur.addClass('d-none');
                bouton_affichage_total_trouv.text(data);

                pouce.toggleClass('btn-secondary ' + (pouce.attr('value') != -1 ? 'btn-success' : 'btn-danger'));
                autre_pouce.removeClass('btn-success btn-danger').addClass('btn-secondary');
            },
            error: function (xhr) {
                bloc_erreur.removeClass('d-none')
                texte_erreur.text(messages_erreur[xhr.status]);
            }
        });
    });
})