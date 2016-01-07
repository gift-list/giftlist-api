from django.conf.urls import url
from users.views import ListCreateUserView, ListCreateAddressView

urlpatterns = [
    url(r'^users/', ListCreateUserView.as_view()),
    url(r'^addresses/', ListCreateAddressView.as_view(), name='lc_address'),
]
