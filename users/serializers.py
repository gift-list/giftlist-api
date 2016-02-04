from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import Address


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name',
                  'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        first_name=validated_data.get('first_name'),
                                        last_name=validated_data.get('last_name')
                                        )

        return user


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('id', 'street', 'street2', 'city', 'state', 'zip')
