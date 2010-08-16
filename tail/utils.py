import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PUBLIC_KEY_FILE = getattr(settings, 'PUBLIC_KEY_FILE',
    os.path.expanduser('~/.ssh/id_rsa.pub'))
try:
    with open(PUBLIC_KEY_FILE, 'r') as f:
        PUBLIC_KEY = f.read().strip()
except (OSError, IOError):
    raise ImproperlyConfigured('You need an SSH public key at %s' % (
        PUBLIC_KEY_FILE,))

def get_public_key():
    return PUBLIC_KEY