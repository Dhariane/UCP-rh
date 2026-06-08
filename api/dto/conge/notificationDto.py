from rest_framework import serializers
from api.models.conge.notification import Notification
from django.utils import timezone


class NotificationDto(serializers.ModelSerializer):

    demandeur_nom = serializers.SerializerMethodField()
    conge_periode = serializers.SerializerMethodField()
    temps_ecoule  = serializers.SerializerMethodField()

    class Meta:
        model  = Notification
        fields = [
            'id',
            'type_notif',
            'titre',
            'message',
            'lu',
            'date_creation',
            'date_lecture',
            'demandeur_nom',
            'conge_periode',
            'temps_ecoule',
            'metadata',
        ]
        read_only_fields = [
            'id',
            'date_creation',
            'date_lecture',
            'demandeur_nom',
            'conge_periode',
            'temps_ecoule',
        ]

    def get_demandeur_nom(self, obj):
        if not obj.conge:
            return None
        p = obj.conge.personnel
        prenom = getattr(p, 'prenom', '') or ''
        nom    = getattr(p, 'nom', '')    or ''
        return f"{prenom} {nom}".strip() or None

    def get_conge_periode(self, obj):
        if not obj.conge:
            return None
        return (
            f"{obj.conge.date_debut.strftime('%d/%m/%Y')} "
            f"→ {obj.conge.date_fin.strftime('%d/%m/%Y')}"
        )

    def get_temps_ecoule(self, obj):
        delta   = timezone.now() - obj.date_creation
        minutes = int(delta.total_seconds() // 60)
        if minutes < 1:
            return "À l'instant"
        if minutes < 60:
            return f"il y a {minutes} min"
        heures = minutes // 60
        if heures < 24:
            return f"il y a {heures} h"
        jours = heures // 24
        return f"il y a {jours} j"