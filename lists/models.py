import locale
from django.contrib.auth.models import User
from django.db import models
from users.models import Address

locale.setlocale( locale.LC_MONETARY, 'en_US.UTF-8' )

class EventList(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
    shipping_address = models.ForeignKey(Address, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    def __str__(self):
        return "{} by {}".format(self.name, self.owner)


class Item(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image_link = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_list = models.ForeignKey(EventList)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # @property
    # def reserved(self):
    #     return self.pledges.aggregate()

    def __str__(self):
        return 'Name: {} Price: {}'.format(self.name, self.price)


class Pledge(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item = models.ForeignKey(Item, related_name='pledges')
    owner = models.ForeignKey(User, related_name='pledges')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} gave {} for {}'.format(self.owner,
                                          locale.currency(self.amount),
                                          self.item.name)

