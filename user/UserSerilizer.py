from datetime import datetime, timedelta

from django.core import exceptions

from rest_framework import serializers
from user.models import User, ResetPasswordToken
import pytz
import django.contrib.auth.password_validation as validators


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    class Meta(object):
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class ResetPasswordTokenSerializerCreate(serializers.ModelSerializer):
    userEmail = serializers.EmailField(read_only=True, allow_blank=False, allow_null=False)



    def create(self, validated_data):
        minutesToExpire = 30

        user = User.objects.filter(email=validated_data['userEmail']).first()

        print(user)
        if user is not None:
            token = ResetPasswordToken.objects.filter(user=user.id).first()

            if token is not None:
                token.delete()

            token = ResetPasswordToken.objects.create(user=user, dateToExpire=(datetime.now() + timedelta(minutes=minutesToExpire)))
            token.save()

            print(token)
            return token
        else:
           return None

    class Meta(object):
        model = ResetPasswordToken
        fields = ["userEmail", "id", "dateToExpire"]

class ResetPasswordTokenSerializer(serializers.ModelSerializer):
    newPassword = serializers.CharField(write_only=True, required=True)
    newPasswordConfirm = serializers.CharField(write_only=True, required=True)


    def isTokenValid(self, token):

        if token is not None:
            dateToExpire = token.dateToExpire

            if dateToExpire > datetime.now().replace(tzinfo=pytz.utc):
                user = User.objects.get(id=token.user_id)

                if user is None:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def changePassword(self, validated_data, user):
        user.set_password(validated_data.get('newPassword'))
        user.save()



    class Meta:
        model = ResetPasswordToken
        fields = ['newPassword', 'newPasswordConfirm']