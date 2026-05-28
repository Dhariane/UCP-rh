import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models.conge.soldeConge import SoldeConge
from api.models.fonction.fonctions import Fonctions
from datetime import date

today = date.today()
annee = today.year

for solde in SoldeConge.objects.filter(is_manual=False):
    fonction = Fonctions.objects.filter(
        personnelle=solde.personnel
    ).order_by('dateDebut').first()

    if not fonction or not fonction.dateDebut:
        continue

    date_debut = fonction.dateDebut

    if date_debut.year == annee:
        mois = today.month - date_debut.month + 1
    else:
        mois = ((annee - date_debut.year) * 12) - date_debut.month + today.month + 1

    solde.total = min(max(mois * 2, 0), 72)
    solde.reste = solde.total - solde.utilise
    solde.save(update_fields=['total', 'reste'])
    print(f"✅ {solde.personnel} → {solde.total}j (embauché {date_debut})")

print("Terminé !")