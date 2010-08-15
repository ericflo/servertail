import struct
from util import xor

__all__ = ['core_hsalsa20', 'stream_salsa20', 'stream_salsa20_xor', 'stream_xsalsa20', 'stream_xsalsa20_xor']

def rotate(x, n):
  x &= 0xffffffff
  return ((x << n) | (x >> (32 - n))) & 0xffffffff

def step(s, i, j, k, r):
  s[i] ^= rotate(s[j] + s[k],r)

def quarterround(s, i0, i1, i2, i3):
  step(s, i1, i0, i3, 7)
  step(s, i2, i1, i0, 9)
  step(s, i3, i2, i1, 13)
  step(s, i0, i3, i2, 18)

def rowround(s):
  quarterround(s, 0, 1, 2, 3)
  quarterround(s, 5, 6, 7, 4)
  quarterround(s, 10, 11, 8, 9)
  quarterround(s, 15, 12, 13, 14)

def columnround(s):
  quarterround(s, 0, 4, 8, 12)
  quarterround(s, 5, 9, 13, 1)
  quarterround(s, 10, 14, 2, 6)
  quarterround(s, 15, 3, 7, 11)

def doubleround(s):
  columnround(s)
  rowround(s)

def rounds(s, n, add=True):
  s1 = list(s)
  while n >= 2:
    doubleround(s)
    n -= 2
  if add:
    for i in range(16): s[i] = (s[i] + s1[i]) & 0xffffffff

o = struct.unpack('<4I', 'expand 32-byte k')

def block(n, k):
  s = [0] * 16
  s[::5] = o
  s[1:5] = k[:4]
  s[6:10] = n
  s[11:15] = k[4:]
  rounds(s, 20)
  return struct.pack('<16I', *s)

def hblock(n, k):
  s = [0] * 16
  s[::5] = o
  s[1:5] = k[:4]
  s[6:10] = n
  s[11:15] = k[4:]
  rounds(s, 20, False)
  return struct.pack('<8I', *(s[::5] + s[6:10]))

def core_hsalsa20(n, k):
  n = struct.unpack('<4I', n)
  k = struct.unpack('<8I', k)
  return hblock(n, k)

def stream_salsa20(l, n, k):
  output = []
  n = struct.unpack('<2I', n)
  k = struct.unpack('<8I', k)
  n = list(n) + [0, 0]
  for i in xrange(0, (l + 63) / 64):
    n[2], n[3] = i & 0xffffffff, i >> 32
    output.append(block(n, k))
  return ''.join(output)[:l]

def stream_salsa20_xor(m, n, k):
  return xor(m, stream_salsa20(len(m), n, k))

def stream_xsalsa20(l, n, k):
  return stream_salsa20(l, n[16:], core_hsalsa20(n[:16], k))

def stream_xsalsa20_xor(m, n, k):
  return xor(m, stream_xsalsa20_xor(len(m), n, k))
