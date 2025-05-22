from rest_framework import serializers
from product.models import SoftSlide, SoftSlideDye, SoftSlideElement, SoftSlideMirror


class SoftSlideElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSlideElement
        fields = "__all__"


class SoftSlideMirrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSlideMirror
        fields = "__all__"

class SoftSlideDyeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSlideDye
        fields = "__all__"



class SoftSlideSerializer(serializers.ModelSerializer):
    mirror = SoftSlideMirrorSerializer(many=False, required=False)
    dye = SoftSlideDyeSerializer(many=False, required=False)
    # elements = serializers.SerializerMethodField()

    class Meta:
        model = SoftSlide
        fields = "__all__"


    def to_representation(self, instance):
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        updated_at = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        data = super().to_representation(instance)

        data["created_at"] = created_at
        data["updated_at"] = updated_at

        data["castle_pos"] = instance.get_castle_pos_display()
        data["plaid_type"] = instance.get_plaid_type_display()

        return data