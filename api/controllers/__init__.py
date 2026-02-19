from .personnelles.propos.personnelleController import PersonnelleController
from .login.loginController import LoginController
from .personnelles.propos.etatCivilController import EtatCivilController
from .personnelles.propos.proposController import ProposController
from .personnelles.propos.sexeController import SexeController
from .personnelles.propos.CinsController import CinsController
from .personnelles.propos.photosController import PhotosController
from .personnelles.banque.agenceController import AgenceController
from .personnelles.banque.banqueController import BanqueController
from .personnelles.banque.coordonneesBancaireController import CoordonneesBancaireController
from .personnelles.contact.contactUrgentController import ContactUrgentController
from .personnelles.contact.relationController import RelationController
from .personnelles.fonction.fonctionController import FonctionController
from .personnelles.fonction.PosteController import PosteController
from .personnelles.fonction.ServiceController import ServiceController
from .personnelles.fonction.superieurController import SuperieurController
from .personnelles.fullController import PersonnelFullController
from .personnelles.propos.familleController import FamilleController

__all__ = [
    "EtatCivilController",
    "ProposController",
    "BanqueController",
    "AgenceController",
    "CoordonneesBancaireController",
    "ContactUrgentController",
    "RelationController",
    "FonctionController",
    "PosteController",
    "ServiceController",
    "SuperieurController",
    "CinsController",
    "PersonnelleController",
    "PhotosController",
    "SexeController",
    "PersonnelFullController",
    "LoginController",
    "FamilleController"
]