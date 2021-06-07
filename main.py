# Cache simulator
import random

WORD_SIZE = 16

# Direct mapped cache
'''
.........................................
| tagSize |    indexSize    |   offset  |
.........................................
'''
class Cache:
    def __init__(self, indexSize, offset):
        # set size variables
        self.indexSize = indexSize
        self.offset = offset
        self.tagSize = WORD_SIZE - indexSize - offset
        # make cache line array
        self.capacity = 2 ** indexSize
        self.array = [None] * self.capacity

    def printInfo(self):
        print("--- Cache Info ---")
        print("Cache capacity: {}".format(self.capacity))
        print("Address format: ", end='')
        print("|....tag:{}....|....indexSize:{}....|....offset:{}....|".format(self.tagSize, self.indexSize, self.offset))
        print("------------------\n")

    def translateAddr(self, addr):
        # make use of binary string
        binStr = bin(addr).replace('0b', '').zfill(WORD_SIZE)
        tagStr = binStr[0 : self.tagSize]
        indexStr = binStr[self.tagSize : self.tagSize+self.indexSize]
        offsetStr = binStr[-self.offset : ]
        tag = int(tagStr, 2)
        index = int(indexStr, 2)
        offset = int(offsetStr, 2)
        return (tag, index, offset)

    # returns result code in string
    def accessAddr(self, addr):
        tag, index, offset = self.translateAddr(addr)
        # cold miss: no entry was there
        if self.array[index] == None:
            self.array[index] = {'tag': tag, 'index': index, 'valid': True}
            return 'coldmiss'
        # entry exists
        else:
            # tag different: always conflict miss (direct mapped)
            if self.array[index]['tag'] != tag:
                self.array[index][tag] = tag
                return 'conflict'
            # else, tag was same so hit
            else:
                return 'hit'

def main():
    cache = Cache(8, 2)
    cache.printInfo()
    
    #tag = 0b0, index = 0b1111, offset = 0b11 
    addr = 0b000000111111
    print("Translate address {} into tag, index, offset".format(addr))
    print(cache.translateAddr(addr))

    print(cache.accessAddr(addr))
    print(cache.accessAddr(addr))
   
    total_cold, total_hit, total_miss = 0, 0, 0
    # test for several random addr
    for i in range(100):
        addr = random.randint(0, 2**WORD_SIZE)        
        print("Access addr: {}", addr)
        print("tag, index, offset : {}", cache.translateAddr(addr))
        result = cache.accessAddr(addr)
        print("result: {}", result)
        if result == 'coldmiss':
            total_cold += 1
        elif result == 'conflict':
            total_miss += 1
        elif result == 'hit':
            total_hit += 1

    print("-----------------------------")
    print("Total result")
    print("Cold misses: {}", total_cold)
    print("Hits: {}", total_hit)
    print("Conflict misses: {}", total_miss)

main()
