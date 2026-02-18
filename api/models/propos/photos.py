from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.personnelles import Personnelles
from django.core.files.base import ContentFile
import base64
from io import BytesIO
from PIL import Image

class Photos(BaseNom):
    data = models.ImageField(upload_to='photos/')
    personnelle = models.ForeignKey(Personnelles, on_delete=models.PROTECT, related_name="photos")

    def save(self, *args, **kwargs):
        if isinstance(self.data, str) and self.data.startswith('data:image/'):
            # Conversion base64 -> fichier image
            format, imgstr = self.data.split(';base64,')
            ext = format.split('/')[-1]
            
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f"photo_{self.personnelle_id}.{ext}"
            )
            self.data = data
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.data)