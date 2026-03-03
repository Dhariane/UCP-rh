from .personnelles.propos.personnelleController import PersonnelleController
from .auth.login.loginController import LoginController
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
from .personnelles.fullController import PersonnelFullController
from .personnelles.propos.familleController import FamilleController
from .personnelles.diplome.experienceController import ExperienceController
from .personnelles.diplome.diplomeController import DiplomeController
from .personnelles.diplome.formationController import FormationController
from .personnelles.diplome.historiqueDuPosteController import HistoriqueDuPosteController
from .personnelles.propos.enfantController import EnfantController
<<<<<<< HEAD
from .personnelles.fonction.contratController import ContratController
from .personnelles.fonction.typeContratController import TypeContratController
from .personnelles.fonction.modefinancementController import ModeFinancementController
=======
from .role.roleController import RoleController     
>>>>>>> dab8f54ee12fb3499d50c57727e71dae74e2d37a
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
    "CinsController",
    "PersonnelleController",
    "PhotosController",
    "SexeController",
    "PersonnelFullController",
    "LoginController",
    "FamilleController",
    "ExperienceController",
    "DiplomeController",
    "FormationController",
    "HistoriqueDuPosteController",
    "EnfantController",
<<<<<<< HEAD
    "ContratController",
    "TypeContratController",
    "ModeFinancementController"
=======
    "LoginController",
    "RoleController"
    
>>>>>>> dab8f54ee12fb3499d50c57727e71dae74e2d37a
]