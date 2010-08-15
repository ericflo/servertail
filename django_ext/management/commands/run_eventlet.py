# TODO: Make this not a management command. I think monkeypatching is happening
#       too late since some Django machinery is already loaded.

import eventlet
import eventlet.wsgi

eventlet.monkey_patch(all=True)

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Use Eventlet to serve this Django app'
    
    def handle_noargs(self, **options):
        app = django.core.handlers.wsgi.WSGIHandler()
        sock = None
        try:
            sock = eventlet.listen(('', 8000))
            eventlet.wsgi.server(sock, app)
        except (KeyboardInterrupt, SystemError):
            if sock:
                sock.close()