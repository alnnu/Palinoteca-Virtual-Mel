from rest_framework import serializers
from app.models import Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"