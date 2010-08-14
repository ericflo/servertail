import datetime

from django.db import models

from django.contrib.auth.models import User

class ServerTail(models.Model):
    hostname = models.TextField()
    port = models.IntegerField(default=22)
    username = models.TextField()
    password = models.TextField(blank=True, default='')
    path = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.hostname