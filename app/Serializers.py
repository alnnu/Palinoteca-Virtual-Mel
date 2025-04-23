from rest_framework import serializers
from app.models import Images, Scenario
from user.models import User
from api.tasks import alanise


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    scenario = ScenarioSerializer(read_only=True)
    def create(self, validated_data):
        file = validated_data.pop('image')

        user = User.objects.filter(id=validated_data["user"]).first()
        imageCreate = Images.objects.create(image=file[0], user=user)


        inferencia = alanise.delay(str(imageCreate.image))

        scenario = Scenario.objects.filter(plant=inferencia.get()).first()

        if scenario is not None:
            imageCreate.scenario = scenario
            imageCreate.save()
        imagesResponse = {"id": str(imageCreate.id), "image": "/media/" + str(imageCreate.image), "scenario": {"id": str(scenario.id), "description": scenario.description, "plant": scenario.plant}}


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

