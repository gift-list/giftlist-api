from rest_framework import generics
from users.permissions import StaffExceptCreate
from users.serializers import UserSerializer


class ListCreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (StaffExceptCreate,)

