from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

import settings


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    picture = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)
    country = CountryField(blank=True)


class Requirements(models.Model):
    flag = models.ImageField(upload_to=settings.STATIC_ROOT)
    nationality = CountryField()
    destination = CountryField()
    visa_required = models.CharField(max_length=20,
        choices=(('required', 'required'),
                 ('not required', 'not required'),
                 ('other', 'other')))
    notes = models.CharField(max_length=1000)


class Trip(models.Model):
    user = models.ForeignKey(User)
    your_requirements = models.ForeignKey(Requirements, related_name="your_requirements_for_trip")
    partner_requirements = models.ForeignKey(Requirements, related_name="partner_requirements_for_trip")
