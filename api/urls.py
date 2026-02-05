from django.urls import path
from api.controllers import PersonnelleController,LoginController,EtatCivilController,ProposController
urlpatterns = [
    path('login', LoginController.as_view(), name='login'),
    path('personnelle', PersonnelleController.as_view(), name='personnelle'),
    path('etat-civils', EtatCivilController.as_view(), name='etat-civils'),
    path("etat-civils/<int:id>/", EtatCivilController.as_view(), name="etatcivil-detail"),
    path('propos', ProposController.as_view(), name='propos'),
    path("propos/<int:id>/", ProposController.as_view(), name="propos-detail"),
]