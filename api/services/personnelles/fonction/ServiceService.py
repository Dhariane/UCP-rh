from  api.models.fonction.service import Services
from api.dto.personnelles.fonction.ServiceDto import ServiceDto

class ServiceService:   
    @staticmethod
    def create(nom: str) -> Services:
        return Services.objects.create(nom=nom)

    @staticmethod
    def getAll():
        return Services.objects.all().order_by("id")
    
    @staticmethod
    def getById(id: int) -> Services:
        return Services.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> Services:   
        service = Services.objects.get(id=id)
        service.nom = nom
        service.save()
        return service
    
    @staticmethod
    def getByIdDto(id: int) -> ServiceDto:  
        service = ServiceService.getById(id)
        return ServiceDto(service)  
    
    @staticmethod
    def getAllDto():        
        services = ServiceService.getAll()
        return ServiceDto(services, many=True)