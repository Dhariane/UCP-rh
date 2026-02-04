from django.urls import path
from api.controllers import PersonnelleController,LoginController,EtatCivilController
urlpatterns = [
    path('login', LoginController.as_view(), name='login'),
    path('personnelle', PersonnelleController.as_view(), name='personnelle'),
    path('etat-civils', EtatCivilController.as_view(), name='etat-civils'),
    path("etat-civils/<int:id>/", EtatCivilController.as_view(), name="etatcivil-detail"),
]