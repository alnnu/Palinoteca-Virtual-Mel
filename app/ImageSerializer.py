from rest_framework import serializers
from app.models import Images, Scenario
from user.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"

class MultiImageSerializer(serializers.ModelSerializer):

    multiImages = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    def create(self, validated_data):
        images = validated_data.pop('multiImages')

        user = User.objects.filter(id=validated_data["user"]).first()
        imagesResponse = []
        for image in images:

            imageCreate = Images.objects.create(image=image,user=user)
            imagesResponse.append({"id": str(imageCreate.id), "image": str(imageCreate.image)})

        return imagesResponse

    class Meta:
        model = Images
        fields = ["id", "user", "multiImages"]

class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = "__all__"