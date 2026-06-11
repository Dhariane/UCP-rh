import api.models.utils.baseNom as baseNoms
<<<<<<< HEAD
from django.db import models


class Banques(baseNoms.BaseNom):
    rib = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.nom}"
=======
class Banques(baseNoms.BaseNom):
    pass
    def __str__(self):
        return f"{(self.nom)}"
>>>>>>> 23088e43 (mon enregistrement local)
