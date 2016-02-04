from collections import namedtuple
from django.contrib.auth.models import User
from lists.models import EventList, Item, Pledge
from lists.serializers import PledgeSerializer
from mock import patch, MagicMock
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ListTestBase(APITestCase):

    def setup_user(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@test.com',
                                             password='password_password')
        return self.user

    def setup_event_list(self, user=None):
        if not user:
            self.setup_user()
            user = self.user

        self.event_list = EventList.objects.create(name='Birthday',
                                                   owner=user,
                                                   active=True)
        return self.event_list

    def setup_item(self, event_list=None):
        if not event_list:
            self.setup_event_list()
            event_list = self.event_list

        self.item = Item.objects.create(name="Motorcycle",
                                        link="http://harleydavidson.com",
                                        image_link="http://flickr.com",
                                        price=1000.00,
                                        event_list=event_list)

        return self.item

    def setup_pledge(self, item=None):
        if not item:
            self.setup_item()
            item = self.item

        self.pledge = item.pledges.create(amount=10.00,
                                          item=item,
                                          owner=self.user)

        return self.pledge


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

    def test_event_list_deactivate(self):
        event_list = EventList.objects.create(name='Birthday',
                                              owner=self.user,
                                              active=True)

        old_deactivate = Item.deactivate
        Item.deactivate = MagicMock()
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=1000.00,
                                   event_list=event_list)

        event_list.deactivate()
        item.deactivate.assert_any_call()
        Item.deactivate = old_deactivate



class ItemTests(ListTestBase):

    def setUp(self):
        self.setup_event_list()

    def test_item_string(self):
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=1000.00,
                                   event_list=self.event_list)

        self.assertTrue("Motorcycle" in str(item))
        self.assertTrue(str(item.price) in str(item))

    def test_item_reserved(self):
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=100.00,
                                   event_list=self.event_list)

        item.pledges.create(amount=10.00,
                            item=item,
                            owner=self.user,
                            status=Pledge.CAPTURED)

        self.assertFalse(item.reserved)

        item.pledges.create(amount=90.00,
                            item=item,
                            owner=self.user,
                            status=Pledge.CAPTURED)

        self.assertTrue(item.reserved)

    def test_deactivate_refund(self):
        """
        Cannot find a better way to test this since everything goes to the
        database to get pledge objects.  Blindly mocking clear across the board
        :return:
        """

        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=100.00,
                                   event_list=self.event_list)

        old_clear = Pledge.clear
        Pledge.clear = MagicMock(return_value=True)

        pledge = item.pledges.create(amount=10.00,
                                     item=item,
                                     owner=self.user,
                                     status=Pledge.CAPTURED)

        item.deactivate()
        pledge.clear.assert_any_call()
        Pledge.clear = old_clear

    def test_deactivate_skip(self):
        item = Item.objects.create(name="Motorcycle",
                                   link="http://harleydavidson.com",
                                   image_link="http://flickr.com",
                                   price=100.00,
                                   event_list=self.event_list)

        old_clear = Pledge.clear
        Pledge.clear = MagicMock(return_value=True)

        pledge = item.pledges.create(amount=100.00,
                                     item=item,
                                     owner=self.user,
                                     status=Pledge.CAPTURED)

        item.deactivate()
        pledge.clear.assert_not_called()
        Pledge.clear = old_clear


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

    @patch('stripe.Refund')
    def test_clear(self, mock_refund):
        # Fake the refund
        mock_refund.create.return_value = {}

        pledge = Pledge.objects.create(amount=10.00,
                                       item=self.item,
                                       owner=self.user,
                                       status=Pledge.CAPTURED)

        pledge.clear()

        self.assertEqual(pledge.status, Pledge.REFUNDED)


class PledgeSerializerTests(ListTestBase):
    def setUp(self):
        self.setup_item()

    @patch('stripe.Charge')
    def test_create(self, mock_charge):

        # We need to mock stripe in the creation
        FakeCharge = namedtuple('FakeCharge', ['stripe_id'])
        mock_charge.create.return_value = FakeCharge("fake_id")

        # Data to create serializer
        data = {'amount': 10.00, 'item': self.item.id, 'owner': self.user.id,
                'status': 'initial', 'token': "abcd"}

        # Data should easily pass so lets check
        serializer = PledgeSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

        # Add a user.  Step is usually done in save of view
        serializer.validated_data['owner'] = self.user
        pledge = serializer.create(serializer.validated_data)
        self.assertEqual(pledge.charge_id, "fake_id")


class ListCreateEventListTests(ListTestBase):
    def setUp(self):
        self.setup_item()

    def test_perform_create(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('eventlist-listcreate'),
                                    data={"name": "Birthday", "active": True})
        self.assertContains(response, self.user.username, status_code=201)


class ListCreatePledgeTests(ListTestBase):
    def setUp(self):
        self.setup_item()

    @patch('stripe.Charge')
    def test_perform_create(self, mock_charge):
        FakeCharge = namedtuple('FakeCharge', ['stripe_id'])
        mock_charge.create.return_value = FakeCharge("fake_id")

        self.client.force_login(self.user)
        response = self.client.post(reverse('lc-pledge'),
                                    data={"amount": 10.00,
                                          "item": self.item.id,
                                          "token": "tok_7lgoDooBPIvvmb"})

        self.assertContains(response, self.user.username, status_code=201)


class DetailUpdateDestroyItemTest(ListTestBase):

    def setUp(self):
        self.setup_pledge()

    def test_perform_destroy(self):
        self.client.force_login(self.user)
        item_id = self.item.id
        pledge_id = self.pledge.id
        self.client.delete(reverse('dud-item', [item_id]))

        item = Item.objects.get(pk=item_id)
        pledge = Pledge.objects.get(pk=pledge_id)

        self.assertTrue(item.deleted)
        self.assertEqual(Pledge.REFUNDED, pledge.status)
