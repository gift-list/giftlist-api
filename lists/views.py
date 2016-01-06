from api.permissions import IsOwnerOrReadOnly
from lists.models import EventList, Item, Pledge
from lists.serializers import EventListSerializer, ItemSerializer, \
    PledgeSerializer
from rest_framework import generics, permissions


class ListCreateEventList(generics.ListCreateAPIView):
    queryset = EventList.objects.all()
    serializer_class = EventListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailUpdateEventList(generics.RetrieveUpdateAPIView):
    queryset = EventList
    serializer_class = EventListSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ListCreateItem(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DetailUpdateDestroyItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_destroy(self, instance):
        instance.pledges.delete()
        instance.delete()


class ListCreatePledge(generics.ListCreateAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DetailUpdateDestroyPledge(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = (IsOwnerOrReadOnly,)