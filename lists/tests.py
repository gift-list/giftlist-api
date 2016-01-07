from django.contrib.auth.models import User
from django.test import TestCase
from lists.models import EventList, Item, Pledge


class EventListTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password_password')

    def test_eventlist_string(self):
        event_list = EventList.objects.create(name='Birthday',
                                              owner=self.user,
                                              active=True)


        self.assertTrue(self.user.username in str(event_list),
                        msg="Missing username")
        self.assertTrue('Birthday' in str(event_list), msg="Missing name")


class ItemTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password_password')
        self.event_list = EventList.objects.create(name='Birthday',
                                              owner=self.user,
                                              active=True)

    def test_item_string(self):
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=1000.00,
                                   event_list = self.event_list)

        self.assertTrue("Motorcycle" in str(item))
        self.assertTrue(str(item.price) in str(item))


class PledgeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password_password')
        self.event_list = EventList.objects.create(name='Birthday',
                                              owner=self.user,
                                              active=True)
        self.item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=1000.00,
                                   event_list = self.event_list)

    def test_pledge_string(self):
        pledge = Pledge.objects.create(amount=10.00,
                                       item=self.item,
                                       owner=self.user)

        self.assertTrue("Motorcycle" in str(pledge))
        self.assertTrue("$10.00" in str(pledge))
        self.assertTrue(self.user.username in str(pledge))