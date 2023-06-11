$(document).ready(function () {
    $('.bouton-suppression').click(function () {
        const reponse = confirm('La suppression d\' un trouv est irréversible. Souhaitez-vous continuer ?');
        if(reponse === false) return;

        let trouv = $(this).closest('.trouv')
        let trouv_id = trouv.attr('aria-id-trouv')

        let redirection = trouv.hasClass('grand-trouv') ? 1 : 0;

        $.ajax({
            url: '/api/trouvs/suppression?id=' + trouv_id + '&redirection='+redirection+'',
            type: 'GET',
            dataType: 'html',
            success: function (data, s, d) {
                if (redirection) window.location.href = '/'
                else trouv.fadeOut(700, () => $(this).remove())
            },
            error: function (xhr) {
                alert('Erreur avec la suppression du trouv. Veuillez réessayer !\nErreur '+xhr.status);
            }
        })
    });

    return true;
});