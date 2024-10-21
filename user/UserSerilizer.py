from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    class Meta(object):
        model = User
        fields = ['id', 'name', 'email', 'password']

