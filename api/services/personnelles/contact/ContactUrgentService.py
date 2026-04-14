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
    def update(id: int, data: dict) -> ContactUrgences:
        try:
            contactUrgence = ContactUrgences.objects.get(id=id)
            
            for key, value in data.items():
                if value is not None:
                    # Si la clé est 'relation' ou 'personnelle', Django REST 
                    # envoie souvent l'objet ou l'ID. On utilise _id pour être sûr.
                    if key in ['relation', 'personnelle']:
                        # Si 'value' est un objet, on prend son ID, sinon on prend la valeur directe
                        val_id = getattr(value, 'id', value)
                        setattr(contactUrgence, f"{key}_id", val_id)
                    else:
                        setattr(contactUrgence, key, value)
            
            contactUrgence.save()
            return contactUrgence
        except ContactUrgences.DoesNotExist:
            raise Exception("Contact d'urgence non trouvé")
    
    @staticmethod
    def getByIdDto(id: int) -> ContactUrgentsDto:
        contactUrgence = ContactUrgencesService.getById(id)
        return ContactUrgentsDto(contactUrgence)
    
    @staticmethod
    def getAllDto():
        contactUrgences = ContactUrgencesService.getAll()
        return ContactUrgentsDto(contactUrgences, many=True)
    