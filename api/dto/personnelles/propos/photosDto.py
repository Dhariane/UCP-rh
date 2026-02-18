from rest_framework import serializers
from api.models.propos.photos import Photos
from api.models.propos.personnelles import Personnelles

class PhotosDto(serializers.ModelSerializer):
    personnelle = serializers.PrimaryKeyRelatedField(queryset=Personnelles.objects.all())
    class Meta:
        model = Photos
        fields = ["id", "nom", "data", "personnelle"]