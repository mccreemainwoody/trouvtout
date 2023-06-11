$(document).ready(function () {
    let form = $('.tableau-edition');
    if (!form.length) return;

    let bloc_message = form.siblings('.alert');
    let message = {
        true: 'Vos modifications ont été sauvegardées avec succès ! La page sera actualisée dans quelques secondes...',
        false: 'Oups ! Une erreur s\'est produite durant l\'enregistrement de vos modifications. Réessayez !'
    };
    let temps_apparition_message = 700;

    bloc_message.hide();

    form.submit(function (event) {
        event.preventDefault()
        if (bloc_message.is(':visible')) return;

        let succes = false;
        let formData = new FormData(this);

        $.ajax({
            url: '/api/trouvs/modification',
            type: 'POST',
            data: formData,
            dataType: 'html',
            processData: false,
            contentType: false,
            success: () => succes = true,
            error: (xhr) => console.log('Erreur avec la suppression du trouv. Erreur ' + xhr.status),
            complete: () => {
                bloc_message.children('p').text(message[succes])
                if (!succes) {
                    bloc_message.removeClass('alert-success').addClass('alert-danger');
                    setTimeout(() => bloc_message.fadeOut(600), 5000 + temps_apparition_message);
                } else {
                    bloc_message.removeClass('alert-danger').addClass('alert-success');
                    $(this).fadeOut(500);
                    setTimeout(() => location.reload(), 2000 + temps_apparition_message);
                }
                bloc_message.fadeIn(temps_apparition_message);
            }
        });
    });
});

