from api.models.propos.photos import Photos
from api.dto.personnelles.propos.photosDto import PhotosDto

class PhotosService:
    @staticmethod
    def create(data_dict) -> Photos:
        # 1. On crée l'objet SANS remplir le champ 'data' (pour éviter l'erreur de limite 100 car.)
        photo_instance = Photos(
            nom = data_dict["nom"][:95], 
            personnelle_id = data_dict["personnelle"]
        )
        
        # 2. On stocke le Base64 dans une variable temporaire "invisible" pour la base de données
        photo_instance._base64_temp = data_dict["data"]
        
        # 3. On appelle .save(), qui va déclencher la conversion dans le modèle
        photo_instance.save() 
        
        return photo_instance
    @staticmethod
    def getAll():
        return Photos.objects.all().order_by("id")
    
    @staticmethod
    def get(id):
        return Photos.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> Photos:
        return Photos.objects.get(id=id)
    
    @staticmethod
    def update(id: int, data, personnelle,nom) -> Photos:  
        photo = Photos.objects.get(id=id)
        photo.nom = nom  
        photo.data = data
        photo.personnelle = personnelle
        photo.save()
        return photo
    
    @staticmethod
    def getByIdDto(id: int) -> PhotosDto:  
        photo = PhotosService.getById(id)
        return PhotosDto(photo)  
    
    @staticmethod
    def getAllDto():        
        photos = PhotosService.getAll()
        return PhotosDto(photos, many=True)