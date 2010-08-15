__all__ = ['verify16', 'verify32']

def verify16(a, b):
  if len(a) != 16 or len(b) != 16:
    raise ValueError('Not 16 bytes')
  return 0 == reduce(lambda x, y: x | y, [ord(a) ^ ord(b) for (a,b) in zip(a,b)])

def verify32(a, b):
  if len(a) != 32 or len(b) != 32:
    raise ValueError('Not 32 bytes')
  return 0 == reduce(lambda x, y: x | y, [ord(a) ^ ord(b) for (a,b) in zip(a,b)])
