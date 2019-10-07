from collections import OrderedDict
import json
import timeit
from array import array
from random import random



symbols = '$¢£¥€¤'

colors = ['black', 'white']
sizes = ['S', 'M', 'L']


if __name__ == "__main__":
    # print(tuple(ord(symbol) for symbol in symbols))
    # tshirts = [(color, size) for color in colors for size in sizes]
    # for tshirts in ('%s %s' % (c, s) for c in colors for s in sizes):
    #     print(tshirts)

    # print(timeit.timeit('"-".join(str(n) for n in range(100))', number=10000))
    # print(timeit.timeit('char in text', setup='text = "sample string"; char = "g"'))
    # board = [['_'] * 3 for i in range(3)]
    # print(board)

    floats = array('d', (random() for i in range(10**7)))
    print(floats[-1])
    with open('floats.bin', 'wb') as f:
        floats.tofile(f)
    
    floats2 = array('d')
    with open('floats.bin', 'rb') as f:
        floats2.fromfile(f, 10**7)
    print(floats2[-1])
    print(floats == floats2)
