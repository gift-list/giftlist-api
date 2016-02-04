import locale
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from users.models import Address
import stripe

locale.setlocale( locale.LC_MONETARY, 'en_US.UTF-8' )


class EventList(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    shipping_address = models.ForeignKey(Address, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    def deactivate(self):
        """
        Deactivates the list by deactivating all items
        :return:
        """

        for item in self.item_set.all():
            item.deactivate()

    def __str__(self):
        return "{} by {}".format(self.name, self.owner)


class Item(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image_link = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_list = models.ForeignKey(EventList)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def deactivate(self):
        """
        Loops through all pledges and requests cleanup if the item isn't already
        reserved
        :return:
        """
        if not self.reserved:
            for pledge in self.pledges.filter(status=Pledge.CAPTURED):
                pledge.clear()

    @property
    def reserved(self) -> bool:
        """
        An item is considered reserved if the total pledges are the same
        as the price of the object.
        :return:
        """
        total = self.pledges.filter(status=Pledge.CAPTURED).aggregate(
                total=Sum('amount'))['total']
        return total >= self.price

    def __str__(self):
        return 'Name: {} Price: {}'.format(self.name, self.price)


class Pledge(models.Model):
    CAPTURED = 'Captured'
    REFUNDED = 'Refunded'
    DISPUTED = 'Disputed'
    INITIAL = 'Intial'
    STATUS_CHOICE = (
        (CAPTURED, 'captured'),
        (REFUNDED, 'refunded'),
        (DISPUTED, 'disputed'),
        (INITIAL, 'initial')
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Item, related_name='pledges')
    owner = models.ForeignKey(User, related_name='pledges')
    status = models.CharField(max_length=15, choices=STATUS_CHOICE,
                              default=INITIAL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    charge_id = models.CharField(max_length=30)

    def clear(self):
        """
        Refund amount and change the status of the pledge only if the pledge is
        in a CAPTURED status
        :return:
        """
        if self.status == self.CAPTURED:
            refund = stripe.Refund.create()

            self.status = self.REFUNDED
            self.save()

    def __str__(self):
        return '{} gave {} for {}'.format(self.owner,
                                          locale.currency(self.amount),
                                          self.item.name)

