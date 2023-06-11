"""trouvtout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import trouvs.views as trouvs
import utilisateurs.views as utilisateurs


urlpatterns = [
    path('admin/', admin.site.urls),
    path('avatar/', include('avatar.urls')),

    path('', trouvs.index, name='index'),
    path('compte/', include('utilisateurs.urls')),
    path('trouvs/', include('trouvs.urls')),
    path('produits/', include('produits.urls')),
]

urlpatterns_connexion = [
    path('connexion', utilisateurs.connexion, name='connexion'),
    path('inscription', utilisateurs.inscription, name='inscription'),
    path('deconnexion', utilisateurs.deconnexion, name='deconnexion'),
    path('mot_de_passe_oublie', utilisateurs.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('recuperation_mot_de_passe', utilisateurs.recuperation_mot_de_passe, name='nouveau_mot_de_passe'),
]

urlpatterns_api = [
    path('api/trouvs/', include('trouvs.urls_api')),
]

urlpatterns += urlpatterns_connexion
urlpatterns += urlpatterns_api
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
