from django.conf.urls import url, include
from lists.views import DetailUpdateEventList, ListCreateEventList, \
    DetailUpdateDestroyItem, ListCreateItem, DetailUpdateDestroyPledge, \
    ListCreatePledge
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^event-lists/(?P<pk>\d+)/', DetailUpdateEventList.as_view()),
    url(r'^event-lists/', ListCreateEventList.as_view(), name='eventlist-listcreate'),
    url(r'^items/(?P<pk>\d+)/', DetailUpdateDestroyItem.as_view()),
    url(r'^items/', ListCreateItem.as_view()),
    url(r'^pledge/(?P<pk>\d+)/', DetailUpdateDestroyPledge.as_view()),
    url(r'^pledge/', ListCreatePledge.as_view(),name='lc-pledge'),
    url(r'^api-token-auth/', views.obtain_auth_token),
]