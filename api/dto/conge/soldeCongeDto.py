from rest_framework import serializers
from api.models.conge.soldeConge import SoldeConge
from api.models.propos.personnelles import Personnelles

class SoldeCongeDTO(serializers.ModelSerializer):
    # ForeignKey avec PrimaryKey
    personnel = serializers.PrimaryKeyRelatedField(queryset=Personnelles.objects.all())
    
    class Meta:
        model = SoldeConge
        fields = [
            'id',
            'personnel',
            'annee',
            'total',
            'utilise',
            'reste',
            'is_manual'
        ]