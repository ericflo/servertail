import datetime
import os

from django.db import models
from django.core.urlresolvers import reverse

from django_ext.crypto import box
from django_ext.utils import cached_property

from django.contrib.auth.models import User

class ServerTail(models.Model):
    hostname = models.TextField()
    port = models.IntegerField(default=22)
    username = models.TextField()
    password = models.TextField(blank=True, default='')
    path = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    
    class Meta(object):
        ordering = ['-date_created']
    
    @cached_property
    def boxed_id(self):
        return box(self.id)
    
    @cached_property
    def filename(self):
        print os.path.split(self.path.split()[0])[1]
        return os.path.split(self.path.split()[0])[1]
    
    def __unicode__(self):
        return self.hostname
    
    def get_absolute_url(self):
        return reverse('tail_tail', args=[self.boxed_id])


class FrontPage(models.Model):
    server_tail = models.ForeignKey(ServerTail)
    date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return u'%s was featured on %s' % (self.server_tail, self.date)