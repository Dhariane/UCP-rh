from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from api.controllers import PersonnelleController,LoginController,EtatCivilController,ProposController
from api.controllers.personnelles.fonction.ServiceController import ServiceController
from api.controllers.personnelles.fonction.PosteController import PosteController
from api.controllers.personnelles.contact.relationController import RelationController
from api.controllers.personnelles.propos.personnelleController import PersonnelleController
from api.controllers.personnelles.contact.contactUrgentController import ContactUrgentController
from api.controllers.personnelles.propos.CinsController import CinsController
from api.controllers.personnelles.fonction.fonctionController import FonctionController
from api.controllers.personnelles.banque.banqueController import BanqueController
from api.controllers.personnelles.banque.agenceController import AgenceController
from api.controllers import PersonnelleController,LoginController,EtatCivilController,SexeController
from api.controllers.personnelles.banque.coordonneesBancaireController import CoordonneesBancaireController
from api.controllers.personnelles.propos.photosController import PhotosController
from api.controllers.personnelles.fonction.superieurController import SuperieurController
urlpatterns = [
    path('login', LoginController.as_view(), name='login'),
    path('personnelle', PersonnelleController.as_view(), name='personnelle'),
    path('etat-civils', EtatCivilController.as_view(), name='etat-civils'),
    path("etat-civils/<int:id>/", EtatCivilController.as_view(), name="etatcivil-detail"),
    path('propos', ProposController.as_view(), name='propos'),
    path("propos/<int:id>/", ProposController.as_view(), name="propos-detail"),

    path("sexes", SexeController.as_view(), name="sexes"),
    path("sexes/<int:id>/", SexeController.as_view(), name="sexe-detail"),
    path("services", ServiceController.as_view(), name="services"),
    path("services/<int:id>/", ServiceController.as_view(), name="service-detail"),
    path("postes", PosteController.as_view(), name="postes"),
    path("postes/<int:id>/", PosteController.as_view(), name="poste-detail"),
    path("relations", RelationController.as_view(), name="relations"),
    path("relations/<int:id>/", RelationController.as_view(), name="relation-detail"),
    path("cins", CinsController.as_view(), name="cins"),
    path("cins/<int:id>/", CinsController.as_view(), name="cins-detail"),
    path("personnelles", PersonnelleController.as_view(), name="personnelles"),
    path("contact-urgents", ContactUrgentController.as_view(), name="contact-urgents"),
    path("contact-urgents/<int:id>/", ContactUrgentController.as_view(), name="contact-urgent-detail"),
    path("fonctions", FonctionController.as_view(), name="fonctions"),
    path("fonctions/<int:id>/", FonctionController.as_view(), name="fonction-detail"),
    path("banques", BanqueController.as_view(), name="banques"),
    path("banques/<int:id>/", BanqueController.as_view(), name="banque-detail"),
    path("agences", AgenceController.as_view(), name="agences"),
    path("agences/<int:id>/", AgenceController.as_view(), name="agence-detail"),
    path("coordonnees-bancaires", CoordonneesBancaireController.as_view(), name="coordonnees-bancaires"),
    path("coordonnees-bancaires/<int:id>/", CoordonneesBancaireController.as_view(), name="coordonnee-bancaire-detail"),
    path("photos", PhotosController.as_view(), name="photos"),
    path("photos/<int:id>/", PhotosController.as_view(), name="photo-detail"),
    path("superieurs",SuperieurController.as_view(), name="superieures")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
