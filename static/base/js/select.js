$(document).ready(function() {
    let url = window.location.href;
    let django_apps = {
        'trouvs': 'trouvs',
        'produits': 'produits',
        'utilisateurs': 'utilisateurs',
    }
    let apps = $('.django-app');

    // Si à la racine du site, on active l'onglet index
    if (url.endsWith('/')) {
        apps.removeClass('active');
        apps.filter('[data-app="index"]').addClass('active');
        return;
    }

    for (let key in django_apps) {
        if (url.indexOf(key) > -1) {
            apps.removeClass('active');
            apps.filter('[data-app="' + django_apps[key] + '"]').addClass('active');
        }
    }
})