from rest_framework import serializers
from api.models.contact.relation import Relations

class RelationDto(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = ["id", "nom","grade"]