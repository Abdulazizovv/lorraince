from botapp.models import BotUser
from rest_framework import serializers

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = "__all__"

    def to_representation(self, instance):
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        data = super().to_representation(instance)
        data["created_at"] = created_at
        data["updated_at"] = updated_at
        return data