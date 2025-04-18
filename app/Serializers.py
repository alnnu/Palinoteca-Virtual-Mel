from rest_framework import serializers
from app.models import Images, Scenario
from user.models import User
from api.tasks import alanise

class ImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        file = validated_data.pop('image')

        user = User.objects.filter(id=validated_data["user"]).first()
        imageCreate = Images.objects.create(image=file[0], user=user)


        inferencia = alanise.delay(str(imageCreate.image))

        senario = Scenario.objects.filter(plant=inferencia.get()).first()

        if senario is not None:
            imageCreate.scenario = senario
            imageCreate.save()
        imagesResponse = {"id": str(imageCreate.id), "image": str(imageCreate.image), "scenario": {"id": str(senario.id), "description": senario.description, "plant": senario.plant}}


        return imagesResponse

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