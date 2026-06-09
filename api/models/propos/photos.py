from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.personnelles import Personnelles
from django.core.files.base import ContentFile
import base64
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class Photos(BaseNom):
    data = models.ImageField(upload_to='photos/')
    personnelle = models.ForeignKey(Personnelles, on_delete=models.CASCADE, related_name="photos")

    def save(self, *args, **kwargs):
        # On vérifie si on a stocké du Base64 dans l'attribut temporaire _base64_temp
        base64_data = getattr(self, '_base64_temp', None)
        
        if base64_data and isinstance(base64_data, str) and base64_data.startswith('data:image/'):
            format, imgstr = base64_data.split(';base64,')
            ext = format.split('/')[-1]
            filename = f"photo_{self.personnelle_id}.{ext}"
            
            # Ici, on remplit le vrai champ 'data' avec le fichier décodé
            # Django va enregistrer le CHEMIN (court) et non le texte (long)
            self.data.save(filename, ContentFile(base64.b64decode(imgstr)), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.data)