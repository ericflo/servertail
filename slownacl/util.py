__all__ = ['xor', 'randombytes']

def xor(s, t):
  output = []
  if len(s) != len(t): raise ValueError('Cannot xor strings of unequal length')
  for i in range(len(s)):
    output.append(chr(ord(s[i]) ^ ord(t[i])))
  return ''.join(output)

def randombytes(n):
  return open('/dev/urandom').read(n)
