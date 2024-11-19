from rest_framework import serializers
from app.models import Images

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
        imagesResponse = []
        for image in images:
            imageCreate = Images.objects.create(image=image)
            imagesResponse.append({"id": str(imageCreate.id), "image": str(imageCreate.image)})

        return imagesResponse

    class Meta:
        model = Images
        fields = ["id", "multiImages"]
