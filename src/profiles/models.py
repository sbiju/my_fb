from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


GENDER_CHOICES = (('M', 'Male'),
                  ('F', 'Female'),
                  ('N', 'Not Disclosed'))


def upload_location(instance, filename):
    return '%s, %s' %(instance.first_name, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="logged_user")
    first_name = models.CharField(max_length=80,blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField()
    phone = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to=upload_location, blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_friend = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profiles:user_detail', kwargs={'pk': self.pk})



