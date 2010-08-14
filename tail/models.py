from django.db import models

from django.contrib.auth.models import User

class ServerTail(models.Model):
    hostname = models.TextField()
    port = models.IntegerField(default=22)
    public_key = models.TextField(blank=True, default='')
    username = models.TextField(blank=True, default='')
    password = models.TextField(blank=True, default='')
    path = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.hostname