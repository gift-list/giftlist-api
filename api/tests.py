from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from django.test import TestCase
from lists.models import EventList
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, \
    force_authenticate


class TestPermissions(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com',
                                             'jiofdajiofas')
        self.user2 = User.objects.create_user('test2', 'test2@test.com',
                                     'jiofdajiofas')

        self.list = EventList.objects.create(name='Christmas', owner=self.user,
                                        active=True)

    def test_isownerreadonly_safe(self):

        factory = APIRequestFactory()
        request = factory.get(reverse('eventlist-listcreate'))

        perm = IsOwnerOrReadOnly()
        self.assertTrue(perm.has_object_permission(request,None, self.list))


    def test_isownerreadonly_owner(self):

        factory = APIRequestFactory()
        request = factory.post(reverse('eventlist-listcreate'))
        request.user = self.user

        perm = IsOwnerOrReadOnly()
        self.assertTrue(perm.has_object_permission(request, None, self.list))

    def test_isownerreadonly_non_owner(self):

        factory = APIRequestFactory()
        request = factory.post(reverse('eventlist-listcreate'))
        request.user = self.user2

        perm = IsOwnerOrReadOnly()
        self.assertFalse(perm.has_object_permission(request, None, self.list))
