from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


RATING_VALUES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), )

class Bailout(models.Model):
    identifier = models.IntegerField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=250)
    party = models.CharField(max_length=25)
    vote_1 = models.CharField(max_length=10, null=True)
    vote_2 = models.CharField(max_length=10, null=True)
    switch = models.CharField(max_length=10, null=True)
    PAC = models.IntegerField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=25)
    bailout_opposition = models.FloatField(max_length=25, null=True, blank=True)
    bailout_support = models.FloatField(max_length=25, null=True, blank=True)
    financial_services_committee = models.IntegerField(max_length=5, null=True, blank=True)


    def __unicode__(self):
        return '{} -- {} -- {} -- {} -- {}'.format(self.identifier, self.name, self.state, self.switch, self.PAC)

class UserProfile(models.Model):
    user = models.OneToOneField(User) # This is the required field to link UserProfile to a User model instance

    # Additional attributes
    zip_code = models.IntegerField(max_length=6)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return '{} -- {} -- {}'.format(self.user.username, self.user.first_name, self.user.last_name)



class Rating(models.Model):
    moc = models.ForeignKey(Bailout)
    user = models.OneToOneField(UserProfile)
    rating = models.IntegerField(default=1, choices=RATING_VALUES)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Rating -- {} -- {} -- {} -- {}'.format(self.user ,self.moc.name, self.moc.state, self.moc.PAC)










    """
    Possible user and rating classes

    class User(models.Models):
        user_name =




    """




