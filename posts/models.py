from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

from osm_field.fields import LatitudeField, LongitudeField, OSMField


class Member(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    contact = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "web_member"
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Location(models.Model):
    # location=models.CharField(max_length=255)
    # location_lat = models.CharField(max_length=22)
    # location_lon =  models.CharField(max_length=22)
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()

    def __str__(self):
        return self.location

    # def get_absolute_url(self):
    #     return reverse("detail", kwargs={"pk": self.pk})

