from rest_framework import serializers
from authentication.models import User


class UserCreation(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            }

    def create(self, validated_data):
        """
        Hash user password and save it to database
        :param validated_data: user input
        :return: User(AbstractUser)
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
