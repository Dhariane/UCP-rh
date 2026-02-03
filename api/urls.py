from django.urls import path
from api.controllers.personnelle.personnelleController import PersonnelleController
from api.controllers.login.loginController import LoginController
urlpatterns = [
    path('login', LoginController.as_view(), name='login'),
    path('personnelle', PersonnelleController.as_view(), name='personnelle')
]