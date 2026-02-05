from django.urls import path

from api.controllers import PersonnelleController,LoginController,EtatCivilController,ProposController
from api.controllers.personnelles.fonction.ServiceController import ServiceController
from api.controllers.personnelles.fonction.PosteController import PosteController
from api.controllers.personnelles.contact.relationController import RelationController
from api.controllers.personnelles.propos.CinsController import CinsController
from api.controllers import PersonnelleController,LoginController,EtatCivilController,SexeController

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
    
]