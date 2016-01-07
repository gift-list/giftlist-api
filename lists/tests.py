from django.contrib.auth.models import User
from django.test import TestCase
from lists.models import EventList, Item, Pledge
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ListTestBase(APITestCase):

    def setup_user(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password_password')

    def setup_event_list(self):
        self.setup_user()
        self.event_list = EventList.objects.create(name='Birthday',
                                                   owner=self.user,
                                                   active=True)

    def setup_item(self):
        self.setup_event_list()
        self.item = Item.objects.create(name="Motorcycle",
                                        link="http://harleydavidson.com",
                                        image_link="http://flickr.com",
                                        price=1000.00,
                                        event_list = self.event_list)

    def setup_pledge(self):
        self.setup_item()
        self.pledge = Pledge.objects.create(amount=10.00,
                                            item=self.item,
                                            owner=self.user)


class EventListTests(ListTestBase):

    def setUp(self):
        self.setup_user()

    def test_event_list_string(self):
        event_list = EventList.objects.create(name='Birthday',
                                              owner=self.user,
                                              active=True)

        self.assertTrue(self.user.username in str(event_list),
                        msg="Missing username")
        self.assertTrue('Birthday' in str(event_list), msg="Missing name")


class ItemTests(ListTestBase):

    def setUp(self):
        self.setup_event_list()

    def test_item_string(self):
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=1000.00,
                                   event_list = self.event_list)

        self.assertTrue("Motorcycle" in str(item))
        self.assertTrue(str(item.price) in str(item))


class PledgeTests(ListTestBase):
    def setUp(self):
        self.setup_item()

    def test_pledge_string(self):
        pledge = Pledge.objects.create(amount=10.00,
                                       item=self.item,
                                       owner=self.user)

        self.assertTrue("Motorcycle" in str(pledge))
        self.assertTrue("$10.00" in str(pledge))
        self.assertTrue(self.user.username in str(pledge))


class ListCreateEventList(ListTestBase):
    def setUp(self):
        self.setup_item()

    def test_perform_create(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('eventlist-listcreate'),
                                    data={"name":"Birthday", "active": True})
        self.assertContains(response, self.user.username, status_code=201)


class ListCreatePledge(ListTestBase):
    def setUp(self):
        self.setup_item()

    def test_perform_create(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('lc-pledge'),
                                    data={"amount": 10.00,
                                          "item": self.item.id})
        self.assertContains(response, self.user.username, status_code=201)


class DetailUpdateDestroyItemTest(ListTestBase):

    def setUp(self):
        self.setup_pledge()

    def test_perform_destroy(self):
        self.client.force_login(self.user)
        item_id = self.item.id
        pledge_id = self.pledge.id
        response = self.client.delete(reverse('dud-item', [item_id]))

        self.assertEqual(0, Item.objects.filter(pk=item_id).count())
        self.assertEqual(0, Pledge.objects.filter(pk=pledge_id).count())



