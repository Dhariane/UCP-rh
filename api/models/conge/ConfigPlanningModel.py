from django.db import models

class ConfigPlanning(models.Model):
    active = models.BooleanField(default=False, verbose_name="Planification Active")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'config_planning'
        verbose_name = "Configuration Planification"

    def __str__(self):
        return f"Planification active : {self.active}"