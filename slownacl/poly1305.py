from verify import verify16

__all__ = ['onetimeauth_poly1305', 'onetimeauth_poly1305_verify']

P = 2 ** 130 - 5

def limb(s):
  return unpack(s) + (1 << 8 * len(s))

def unpack(s):
  return sum(ord(s[i]) << 8 * i for i in range(len(s)))

def pack(n):
  return ''.join([chr(n >> 8 * i & 255) for i in range(16)])

def onetimeauth_poly1305(m, k):
  if len(k) != 32: raise ValueError('Invalid Poly1305 key')
  r = unpack(k[:16]) & 0x0ffffffc0ffffffc0ffffffc0fffffff

  h = 0
  for i in range(0, len(m), 16):
    c = limb(m[i:i+16])
    h = (h + c) * r % P
  h += unpack(k[16:])

  return pack(h)

def onetimeauth_poly1305_verify(a, m, k):
  return verify16(a, onetimeauth_poly1305(m, k))
