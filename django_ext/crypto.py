import base64

from django.conf import settings

from slownacl import secretbox_xsalsa20poly1305_open
from slownacl import secretbox_xsalsa20poly1305, auth_hmacsha512, hash_sha512

KEY = auth_hmacsha512('django_ext.crypto',
    hash_sha512(settings.SECRET_KEY)[:32])
KEY2 = auth_hmacsha512('django_ext.crypto.key2',
    hash_sha512(settings.SECRET_KEY)[:32])

NONCE_PAD = '\0' * 12

memo_box = {}
memo_unbox = {}
MAX_MEMO = 1000

def _memo(i, resp):
    memo_box[i] = resp
    memo_unbox[resp] = i
    if len(memo_box) > MAX_MEMO:
        min_i = min(memo_box.keys())
        memo_unbox.pop(memo_box[min_i], None)
        memo_box.pop(min_i, None)

def box(i):
    i = int(i)
    if i in memo_box:
        return memo_box[i]
    nonce = auth_hmacsha512(str(i), KEY2)[:12]
    c = secretbox_xsalsa20poly1305(str(i), nonce + NONCE_PAD, KEY)
    resp = base64.urlsafe_b64encode(nonce + c)
    _memo(i, resp)
    return resp

def unbox(encoded):
    if encoded in memo_unbox:
        return memo_unbox[encoded]
    s = base64.urlsafe_b64decode(encoded)
    encoded = base64.urlsafe_b64encode(s) # Fixes EvilPacket haxxx0r
    m = secretbox_xsalsa20poly1305_open(s[12:], s[:12] + NONCE_PAD, KEY)
    resp = int(m)
    _memo(resp, encoded)
    return resp