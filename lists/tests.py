from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from users.permissions import StaffExceptCreate


class TestUserPermissions(APITestCase):

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
