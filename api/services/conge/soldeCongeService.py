from api.models.conge.soldeConge import SoldeConge


class SoldeCongeServices:

    @staticmethod
    def getAll():
        return SoldeConge.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> SoldeConge:
        return SoldeConge.objects.get(id=id)

    @staticmethod
    def create(data) -> SoldeConge:
        return SoldeConge.objects.create(
            personnel=data.get("personnel"),
            annee=data.get("annee"),
            total=data.get("total", 0),
            reste=data.get("reste", 0),
            is_manual=data.get("is_manual", False),  # ← ajouté
        )

    @staticmethod
    def update(id: int, data) -> SoldeConge:
        solde = SoldeConge.objects.get(id=id)

        fields_to_update = []

        if "annee" in data:
            solde.annee = data["annee"]
            fields_to_update.append("annee")

        if "total" in data:
            solde.total = data["total"]
            fields_to_update.append("total")
            # ✅ Si les RH modifient le total manuellement → verrouiller
            solde.is_manual = True
            fields_to_update.append("is_manual")

        if "utilise" in data:
            solde.utilise = data["utilise"]
            fields_to_update.append("utilise")

        if "reste" in data:
            solde.reste = data["reste"]
            fields_to_update.append("reste")

        if "personnel" in data:
            solde.personnel = data["personnel"]
            fields_to_update.append("personnel")

        # Permettre de repasser en automatique explicitement
        if "is_manual" in data:
            solde.is_manual = data["is_manual"]
            if "is_manual" not in fields_to_update:
                fields_to_update.append("is_manual")

        if fields_to_update:
            solde.save(update_fields=fields_to_update)

        return solde