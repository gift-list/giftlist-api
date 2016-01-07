from django.contrib.auth.models import User
from django.db import models
from localflavor.us.models import USStateField, USZipCodeField


class UserProfile(models.Model):

    user = models.ForeignKey(User)
    avatar = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return "User: {} profile".format(self.user.username)


class Address(models.Model):
    street = models.CharField(max_length=200)
    street2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = USStateField()
    zip = USZipCodeField()
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}, {}".format(self.street, self.city, self.state,
                                     self.zip)
