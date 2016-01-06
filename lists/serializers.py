from django.contrib.auth.models import User
from lists.models import EventList, Item, Pledge
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class EventListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = EventList
        fields = ('name', 'owner', 'created_at')


class ItemSerializer(serializers.ModelSerializer):
    event_list = EventListSerializer()

    class Meta:
        model = Item
        fields = ('name', 'link', 'image_link', 'price', 'event_list',
                  'created_at', 'modified_at')


class PledgeSerializer(serializers.ModelSerializer):
    pledger = UserSerializer()

    class Meta:
        model = Pledge
        fields = ('amount', 'item', 'pledger', 'created_at', 'modified_at')

