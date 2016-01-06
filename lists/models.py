from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class EventList(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
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
        return '{} gave {} for {}'.format(self.pledger, self.amount, self.item)

