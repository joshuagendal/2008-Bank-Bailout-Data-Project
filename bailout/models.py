from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField


RATING_VALUES = ((1, 1), (2, 2),
                 (3, 3), (4, 4), (5, 5))
POLITICAL_PARTY = (('Democrat', 'Democrat'), ('Republican', 'Republican'))



class Bailout(models.Model):
    identifier = models.IntegerField(max_length=5, null=True, blank=True)
    name = models.CharField(max_length=250)
    party = models.CharField(max_length=25)
    vote_1 = models.CharField(max_length=10, null=True)
    vote_2 = models.CharField(max_length=10, null=True)
    switch = models.CharField(max_length=10, null=True)
    PAC = models.IntegerField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=25) # CHANGE TO ABBREVIATIONS
    state_ab = models.CharField(max_length=2)
    bailout_opposition = models.FloatField(max_length=25, null=True, blank=True)
    bailout_support = models.FloatField(max_length=25, null=True, blank=True)
    financial_services_committee = models.IntegerField(max_length=5, null=True, blank=True)
    ada_score = models.IntegerField(max_length=2, null=True, blank=True)
    swing_district = models.FloatField(max_length=10, null=True, blank=True)
    win_margin_06 = models.FloatField(max_length=5, null=True, blank=True)



    def __unicode__(self):
        return '{} -- {} -- {} -- {} -- {}'.format(self.identifier, self.name, self.state, self.switch, self.PAC)


    def get_avg_ratings(self):
        if not self.rating_set.count():
            return 'No ratings for {}'.format(self.name)
        else:
            dummy = 0
            for i in self.rating_set.all():
                dummy += i.rating
            return dummy / self.rating_set.count()


class UserProfile(models.Model):
    user = models.OneToOneField(User) # This is the required field to link UserProfile to a User model instance

    # Additional attributes
    zip_code = models.IntegerField(max_length=6) # change to state
    picture = models.ImageField(upload_to='profile_images', blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    political_party = models.CharField(default='None', choices=POLITICAL_PARTY, max_length=50)
    state = USStateField()

    def __unicode__(self):
        return '{} -- {} -- {}'.format(self.user.username, self.user.first_name, self.user.last_name)




class Rating(models.Model):
    moc = models.ForeignKey(Bailout, on_delete=models.CASCADE, verbose_name='Member of Congress')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, choices=RATING_VALUES)
    created = models.DateTimeField(auto_now_add=True, null=True)
    # unique_together - way to allow users to rate each member only once

    def __unicode__(self):
        return 'Rating -- {} -- {} -- {} -- {} -- {}'.format(self.user.username, self.moc.name, self.rating, self.moc.state, self.moc.PAC)













