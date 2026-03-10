from .personnelles.fonction.ServiceService import ServiceService
from .personnelles.contact.RelationService import RelationService
from .personnelles.banque import agencesService
from .personnelles.banque import coordonneesBancaireServices
from .personnelles.banque import banqueService
from .personnelles.contact import ContactUrgentService
from .personnelles.fonction import fonctionService
from .personnelles.fonction import PosteService
from .personnelles.propos import CinsService
from .personnelles.propos import etatCivilService
from .personnelles.propos import personnellesService
from .personnelles.propos import photosService
from .personnelles.propos import proposService
from .personnelles.propos import sexeService
from .personnelles.diplome import experienceService
from .personnelles.diplome import diplomeService
from .personnelles.diplome import formationService
from .personnelles.diplome import historiqueDuPosteService
from .personnelles.propos import enfantService
__all__ = [
    "personnellesService",
    "sexeService",
    "CinsService",
    "photosService",
    "RelationService",
    "agencesService",
    "banqueService",
    "ContactUrgentService",
    "fonctionService",
    "PosteService",
    "proposService",
    "etatCivilService",
    "ServiceService",
    "coordonneesBancaireServices",
    "experienceService",
    "diplomeService",
    "formationService",
    "historiqueDuPosteService",
    "enfantService"
    
]
