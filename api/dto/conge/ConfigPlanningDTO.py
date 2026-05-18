from rest_framework import serializers

class ConfigPlanningDTO(serializers.Serializer):
    active = serializers.BooleanField(required=True)
    updated_at = serializers.DateTimeField(read_only=True, required=False)