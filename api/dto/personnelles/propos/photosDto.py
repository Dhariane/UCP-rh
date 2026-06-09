from rest_framework import serializers
from api.models.propos.photos import Photos

class PhotosDto(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = [
            "id",
            "nom",
            "data",
            "personnelle"
        ]