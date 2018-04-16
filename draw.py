import numpy as np
import matplotlib.pyplot as plt

# l1 and l2 cache size
# l1 2**5 32k
# l2 2**8 256k
l1 = 5
l2 = 8

def parse(raw):
  x, y, z = [], [], []
  lines = raw.split('\n')
  for aa in lines:
    if aa is '': break
    bb = aa.split('|')
    a = int(bb[0])
    b = float(bb[1].split('ns')[0])
    c = float(bb[2][2:].split()[0])
    x.append(a)
    y.append(b)
    z.append(c)
  #return (np.array(x), np.array(y), np.array(z))
  return x, y, z

def cache_random():
  name = 'random.out'
  # Set x axis's ticks 
  ticks,loc = [],[]
  for i in range(7, 25, 2):
    n = 2**(i+3)
    loc.append(i)
    if n >= 2**20:
      ticks.append(str(n//2**20)+'M')
    else:
      ticks.append(str(n//2**10)+'k')

  f = open(name)
  x, y, z = parse(f.read())

  plt.figure(1, figsize=(12, 7))
  plt.subplot(231)
  plt.title('Cache randomly access')
  plt.plot(x, z, '^-', [7+l1, 7+l2], [z[l1], z[l2]], 'r^')
  plt.ylabel('Cycles / access')
  plt.xlabel('Workset size')
  plt.xticks(loc, ticks)
  #plt.savefig('./random.png')

def cache_sequential():
  name = 'seq.out'
  # Set x axis's ticks 
  ticks,loc = [],[]
  for i in range(7, 25, 2):
    n = 2**(i+3)
    loc.append(i)
    if n >= 2**20:
      ticks.append(str(n//2**20)+'M')
    else:
      ticks.append(str(n//2**10)+'k')

  f = open(name)
  x, y, z = parse(f.read())

  plt.subplot(232)
  plt.title('Cache sequentially access')
  plt.plot(x, z, '^-', [7+l1, 7+l2], [z[l1], z[l2]], 'r^')
  axes = plt.gca()
  axes.set_ylim([0,10])
  plt.ylabel('Cycles / access')
  plt.xlabel('Workset size')
  plt.xticks(loc, ticks)
  #plt.savefig('./random.png')
  #plt.show()

def tlb_random():
  name = 'tlb-random.out'
  # Set x axis's ticks 
  ticks,loc = [],[]
  for i in range(10, 28, 2):
    n = 2**(i)
    loc.append(i)
    if n >= 2**20:
      ticks.append(str(n//2**20)+'M')
    else:
      ticks.append(str(n//2**10)+'k')

  f = open(name)
  x, y, z = parse(f.read())

  plt.subplot(233)
  plt.title('TLB randomly access')
  plt.plot(x, z, '^-', [10+l1, 10+l2], [z[l1], z[l2]], 'r^')
  plt.ylabel('Cycles / access')
  plt.xlabel('Workset size')
  plt.xticks(loc, ticks)
  #plt.savefig('./random.png')
  #plt.show()

def tlb_sequential():
  name = 'tlb-seq.out'

  # Set x axis's ticks 
  ticks,loc = [],[]
  for i in range(10, 28, 2):
    n = 2**i
    loc.append(i)
    if n >= 2**20:
      ticks.append(str(n//2**20)+'M')
    else:
      ticks.append(str(n//2**10)+'k')

  f = open(name)
  x, y, z = parse(f.read())

  plt.subplot(234)
  plt.title('TLB sequentially access')
  plt.plot(x, z, '^-', [10+l1, 10+l2], [z[l1], z[l2]], 'r^')
  plt.ylabel('Cycles / access')
  plt.xlabel('Workset size')
  plt.xticks(loc, ticks)
  #plt.savefig('./random.png')
  #plt.show()

def cache_line():
  name = 'cache-line.out'
  f = open(name)
  x, y, z = parse(f.read())

  # Set x axis's ticks 
  ticks,loc = [],[]
  i = 1
  while (i <= 1024):
    if i in [32] or i >= 256:
      loc.append(i)
      ticks.append(str(i))
    i = 2*i

  plt.subplot(235)
  plt.plot(x, y, '^-')
  plt.xticks(loc, ticks)
  plt.subplots_adjust(top=0.92, bottom=0.06, left=0.1, right=0.95, hspace=0.3,
                    wspace=0.35)
  plt.savefig('./result.png')
  plt.show()

if __name__ == '__main__':
  cache_random()
  cache_sequential()
  tlb_random()
  tlb_sequential()
  cache_line()