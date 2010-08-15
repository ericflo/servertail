import base64

from django.conf import settings

from slownacl import secretbox_xsalsa20poly1305_open
from slownacl import secretbox_xsalsa20poly1305, auth_hmacsha512, hash_sha512

KEY = auth_hmacsha512('django_ext.crypto',
    hash_sha512(settings.SECRET_KEY)[:32])
KEY2 = auth_hmacsha512('django_ext.crypto.key2',
    hash_sha512(settings.SECRET_KEY)[:32])

NONCE_PAD = '\0' * 12

def box(i):
    nonce = auth_hmacsha512(str(i), KEY2)[:12]
    c = secretbox_xsalsa20poly1305(str(i), nonce + NONCE_PAD, KEY)
    return base64.urlsafe_b64encode(nonce + c)

def unbox(s):
    s = base64.urlsafe_b64decode(s)
    m = secretbox_xsalsa20poly1305_open(s[12:], s[:12] + NONCE_PAD, KEY)
    return int(m)