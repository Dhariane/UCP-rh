from rest_framework import serializers
from api.models.contact.contactUrgences import ContactUrgences

class ContactUrgentsDto(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgences
        fields = ["id", "nom", "telephone", "adresse", "relation", "personnelle"]