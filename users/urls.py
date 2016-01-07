from django.conf.urls import url
from users.views import ListCreateUserView

urlpatterns = [
    url(r'^users/', ListCreateUserView.as_view()),
]
