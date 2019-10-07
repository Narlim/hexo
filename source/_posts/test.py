from collections import OrderedDict
import json
import timeit



symbols = '$¢£¥€¤'

colors = ['black', 'white']
sizes = ['S', 'M', 'L']


if __name__ == "__main__":
    # print(tuple(ord(symbol) for symbol in symbols))
    # tshirts = [(color, size) for color in colors for size in sizes]
    for tshirts in ('%s %s' % (c, s) for c in colors for s in sizes):
        print(tshirts)

    # print(timeit.timeit('"-".join(str(n) for n in range(100))', number=10000))
    # print(timeit.timeit('char in text', setup='text = "sample string"; char = "g"'))
    board = [['_'] * 3 for i in range(3)]
    print(board)