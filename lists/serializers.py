from django.contrib.auth.models import User
from lists.models import EventList, Item, Pledge
from rest_framework import serializers
from users.serializers import UserSerializer
import stripe


class EventListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = EventList
        fields = ('name', 'owner', 'active', 'shipping_address', 'created_at')


class ItemSerializer(serializers.ModelSerializer):
    event_list = EventListSerializer()

    class Meta:
        model = Item
        fields = ('name', 'link', 'image_link', 'price', 'event_list',
                  'created_at', 'modified_at')


class PledgeSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    token = serializers.CharField(max_length=30, write_only=True, required=True)

    def create(self, validated_data):
        """
        This overrides to insert stripe calls to convert the one use token
        into a full charge token
        :param validated_data:
        :return:
        """
        token = validated_data.pop("token")
        amount = int(validated_data['amount']) * 100

        charge = stripe.Charge.create(amount=amount, currency="usd",
                                      source=token,
                                      description="Payment for item {}"
                                      .format(validated_data['item'].id))

        return Pledge.objects.create(charge_id=charge.stripe_id,
                                     **validated_data)

    class Meta:
        model = Pledge
        fields = ('amount', 'item', 'owner', 'token', 'created_at',
                  'modified_at')

