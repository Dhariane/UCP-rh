from api.models.propos.photos import Photos
from api.dto.personnelles.propos.photosDto import PhotosDto

class PhotosService:
    @staticmethod
    def create(data) -> Photos:
        return Photos.objects.create(
            nom = data["nom"],
            data = data["data"],
            personnelle_id=data["personnelle"]
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