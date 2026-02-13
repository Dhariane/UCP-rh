from api.models.contact.contactUrgences import ContactUrgences
from api.dto.personnelles.contact.ContactUrgentsDto import ContactUrgentsDto

class ContactUrgencesService:    
    def create(data):
        return ContactUrgences.objects.create(
            nom= data['nom'],
            telephone=data["telephone"],
            adresse=data["adresse"],
            personnelle=data["personnelle"],
            relation=data["relation"]
            
        )
    @staticmethod
    def getAll():
        return ContactUrgences.objects.all().order_by("id")
    
    @staticmethod
    def get(id):
        return ContactUrgences.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> ContactUrgences:
        return ContactUrgences.objects.get(id=id)
    
    @staticmethod
    def update(id: int, telephone: str, adresse: str, personnelle_id: int, relation_id: int) -> ContactUrgences:
        contactUrgence = ContactUrgences.objects.get(id=id)
        contactUrgence.telephone = telephone
        contactUrgence.adresse = adresse
        contactUrgence.personnelle = personnelle_id 
        contactUrgence.relation = relation_id
        contactUrgence.save()
        return contactUrgence
    
    @staticmethod
    def getByIdDto(id: int) -> ContactUrgentsDto:
        contactUrgence = ContactUrgencesService.getById(id)
        return ContactUrgentsDto(contactUrgence)
    
    @staticmethod
    def getAllDto():
        contactUrgences = ContactUrgencesService.getAll()
        return ContactUrgentsDto(contactUrgences, many=True)
    