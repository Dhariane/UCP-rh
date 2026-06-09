from api.models.conge.ConfigPlanningModel import ConfigPlanning # Ta table de config globale

class ConfigPlanningService:

    @classmethod
    def get_or_create_config(cls):
        config, _ = ConfigPlanning.objects.get_or_create(id=1, defaults={'active': False})
        return config

    @classmethod
    def update_status(cls, active_status):
        config = cls.get_or_create_config()
        config.active = active_status
        config.save()
        return config