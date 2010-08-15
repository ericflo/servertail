from util import xor, randombytes
from salsa20 import stream_salsa20
from sha512 import hash_sha512, auth_hmacsha512, auth_hmacsha512_verify
from curve25519 import smult_curve25519, smult_curve25519_base

__all__ = ['secretbox_salsa20hmacsha512', 'secretbox_salsa20hmacsha512_open', 'box_curve25519salsa20hmacsha512_keypair', 'box_curve25519salsa20hmacsha512', 'box_curve25519salsa20hmacsha512_open', 'box_curve25519salsa20hmacsha512_beforenm', 'box_curve25519salsa20hmacsha512_afternm', 'box_curve25519salsa20hmacsha512_open_afternm']

def secretbox_salsa20hmacsha512(m, n, k):
  s = stream_salsa20(len(m) + 32, n, k)
  c = xor(m, s[32:])
  a = auth_hmacsha512(c, s[:32])
  return a + c

def secretbox_salsa20hmacsha512_open(c, n, k):
  if len(c) < 32: raise ValueError('Too short for Salsa20HMACSHA512 box')
  s = stream_salsa20(32, n, k)
  if not auth_hmacsha512_verify(c[:32], c[32:], s):
    raise ValueError('Bad authenticator for Salsa20HMACSHA512 box')
  s = stream_salsa20(len(c), n, k)
  return xor(c[32:], s[32:])


def box_curve25519salsa20hmacsha512_keypair():
  sk = randombytes(32)
  pk = smult_curve25519_base(sk)
  return (pk, sk)

def box_curve25519salsa20hmacsha512(m, n, pk, sk):
  return box_curve25519salsa20hmacsha512_afternm(
    m, n, box_curve25519salsa20hmacsha512_beforenm(pk, sk))

def box_curve25519salsa20hmacsha512_open(c, n, pk, sk):
  return box_curve25519salsa20hmacsha512_open_afternm(
    c, n, box_curve25519salsa20hmacsha512_beforenm(pk, sk))

def box_curve25519salsa20hmacsha512_beforenm(pk, sk):
    return hash_sha512(smult_curve25519(sk, pk))[:32]

def box_curve25519salsa20hmacsha512_afternm(m, n, k):
  return secretbox_salsa20hmacsha512(m, n, k)

def box_curve25519salsa20hmacsha512_open_afternm(c, n, k):
  return secretbox_salsa20hmacsha512_open(c, n, k)
