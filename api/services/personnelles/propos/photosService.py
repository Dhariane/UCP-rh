from api.models.propos.photos import Photos
from api.dto.personnelles.propos.photosDto import PhotosDto

class PhotosService:
    @staticmethod
    def create(data_dict) -> Photos:
        return Photos.objects.create(
            nom=data_dict["nom"][:95],
            personnelle_id=data_dict["personnelle"],
            data=data_dict["data"] # On met le fichier directement dans le champ ImageField
        )
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