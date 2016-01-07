from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from users.models import Address
from users.permissions import StaffExceptCreate


class UserPermissionsTests(APITestCase):

    def setUp(self):

        # Set up the users
        self.staff = User.objects.create_user(username="staff",
                                              email="staff@test.com",
                                              password="jiofjsoafodjas123")
        self.staff.is_staff = True

        self.user = User.objects.create_user(username="user",
                                             email="user@test.com",
                                             password="jiofjsoafodjas123")

    def test_StaffExceptCreate_post(self):
        permission = StaffExceptCreate()

        factory = APIRequestFactory()
        request = factory.post('/test/', data={})
        request.user = self.user

        self.assertTrue(permission.has_permission(request, None))

        # Now run with staff member to get the same result
        request.user = self.staff
        self.assertTrue(permission.has_permission(request, None))

    def test_StaffExceptCreate_get(self):
        permission = StaffExceptCreate()

        factory = APIRequestFactory()
        request = factory.get('/test/')

        # First make sure staff can access
        request.user = self.staff
        self.assertTrue(permission.has_permission(request, None))

        # Make sure the user cannot get into the system
        request.user = self.user
        self.assertFalse(permission.has_permission(request, None))


class ListCreateAddressView(APITestCase):

    def setUp(self):
        # Set up the users
        self.staff = User.objects.create_user(username="staff",
                                              email="staff@test.com",
                                              password="jiofjsoafodjas123",
                                              is_staff=True)

        self.user = User.objects.create_user(username="user",
                                             email="user@test.com",
                                             password="jiofjsoafodjas123")

        # Create the addresses
        Address.objects.create(street='221B Baker Street',
                               city='Las Vegas',
                               state='NV',
                               zip=89123,
                               owner=self.user)
        Address.objects.create(street='1600 Pennsylvania Ave NW',
                               city='Washington',
                               state='DC',
                               owner=self.staff)

    def test_queryset_filter(self):

        # test the staff
        self.client.force_login(self.staff)
        response = self.client.get(reverse('lc_address'))
        self.assertContains(response, "1600")
        self.assertContains(response, "221B")

        # test a normal user
        self.client.force_login(self.user)
        response = self.client.get(reverse('lc_address'))
        self.assertNotContains(response, "1600")
        self.assertContains(response, "221B")
