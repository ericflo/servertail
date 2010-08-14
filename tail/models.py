from django.db import models

from django.contrib.auth.models import User

class Server(models.Model):
    hostname = models.TextField()
    public_key = models.TextField(blank=True, default='')
    username = models.TextField(blank=True, default='')
    password = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.hostname


class FilePath(models.Model):
    path = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.path