from util import xor, randombytes
from salsa20 import core_hsalsa20, stream_xsalsa20
from poly1305 import onetimeauth_poly1305, onetimeauth_poly1305_verify
from curve25519 import smult_curve25519, smult_curve25519_base

__all__ = ['secretbox_xsalsa20poly1305', 'secretbox_xsalsa20poly1305_open', 'box_curve25519xsalsa20poly1305_keypair', 'box_curve25519xsalsa20poly1305', 'box_curve25519xsalsa20poly1305', 'box_curve25519xsalsa20poly1305_open', 'box_curve25519xsalsa20poly1305_beforenm', 'box_curve25519xsalsa20poly1305_afternm', 'box_curve25519xsalsa20poly1305_open_afternm']

def secretbox_xsalsa20poly1305(m, n, k):
  s = stream_xsalsa20(32 + len(m), n, k)
  c = xor(m, s[32:])
  a = onetimeauth_poly1305(c, s[:32])
  return a + c

def secretbox_xsalsa20poly1305_open(c, n, k):
  if len(c) < 16: raise ValueError('Too short for XSalsa20Poly1305 box')
  s = stream_xsalsa20(32, n, k)
  if not onetimeauth_poly1305_verify(c[:16], c[16:], s):
    raise ValueError('Bad authenticator for XSalsa20Poly1305 box')
  s = stream_xsalsa20(16 + len(c), n, k)
  return xor(c[16:], s[32:])


def box_curve25519xsalsa20poly1305_keypair():
  sk = randombytes(32)
  pk = smult_curve25519_base(sk)
  return (pk, sk)

def box_curve25519xsalsa20poly1305(m, n, pk, sk):
  return box_curve25519xsalsa20poly1305_afternm(
      m, n, box_curve25519xsalsa20poly1305_beforenm(pk, sk))

def box_curve25519xsalsa20poly1305_open(c, n, pk, sk):
  return box_curve25519xsalsa20poly1305_open_afternm(
      c, n, box_curve25519xsalsa20poly1305_beforenm(pk, sk))

def box_curve25519xsalsa20poly1305_beforenm(pk, sk):
  return core_hsalsa20('\0' * 16, smult_curve25519(sk, pk))

def box_curve25519xsalsa20poly1305_afternm(m, n, k):
  return secretbox_xsalsa20poly1305(m, n, k)

def box_curve25519xsalsa20poly1305_open_afternm(c, n, k):
  return secretbox_xsalsa20poly1305_open(c, n, k)
