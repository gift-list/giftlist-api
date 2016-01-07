from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.models import Address
from users.permissions import StaffExceptCreate
from users.serializers import UserSerializer, AddressSerializer


class ListCreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (StaffExceptCreate,)


class ListCreateAddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        if self.request.user.is_staff:
            return Address.objects.all()
        else:
            return Address.objects.filter(owner=self.request.user)



