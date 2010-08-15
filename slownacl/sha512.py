import hashlib
from util import xor
from verify import verify32

__all__ = ['hash_sha512', 'auth_hmacsha512', 'auth_hmacsha512_verify']

# Python has an hmac module, but at least as of 2.5.1, it assumed a
# block size of 64 bytes regardless of hash function, whereas SHA-512
# uses a block size of 128 bytes.

def hash_sha512(m):
  return hashlib.sha512(m).digest()

def auth_hmacsha512(m, k):
  if len(k) != 32: raise ValueError('Invalid key size for HMACSHA512')
  def pad(c): return xor(chr(c) * 128, k + '\0' * 96)
  m = hash_sha512(pad(0x36) + m)
  m = hash_sha512(pad(0x5c) + m)
  return m[:32]

def auth_hmacsha512_verify(a, m, k):
  return verify32(a, auth_hmacsha512(m, k))
