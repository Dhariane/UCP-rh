from rest_framework import serializers
from api.models import Enfant
from datetime import date

class EnfantDTO(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = Enfant
        fields = ['id', 'nom', 'prenom', 'dateNaissance', 'lieuNaissance', 'personnelle', 'age']

    def get_age(self, obj):
        # On récupère la date de naissance
        d_naissance = obj.dateNaissance
        
        # Sécurité : Si c'est une chaîne de caractères (str), 
        # on ne fait rien ici pour éviter l'erreur .year
        # Mais normalement, après enregistrement, Django donne un objet date.
        if not d_naissance or isinstance(d_naissance, str):
            # Si c'est du texte, on essaie de le convertir proprement
            try:
                from django.utils.dateparse import parse_date
                d_naissance = parse_date(str(d_naissance))
            except:
                return None

        if d_naissance:
            today = date.today()
            # Calcul de l'âge
            age = today.year - d_naissance.year - (
                (today.month, today.day) < (d_naissance.month, d_naissance.day)
            )
            return age
            
        return None