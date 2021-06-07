WORD_SIZE = 32

# Direct mapped cache
class DirectMappedCache:
    def __init__(self, indexSize, offset):
        # set size variables
        self.indexSize = indexSize
        self.offset = offset
        self.tagSize = WORD_SIZE - indexSize - offset
        # make cache line array
        self.capacity = 2 ** indexSize
        self.array = [None] * self.capacity

    def printInfo(self):
        print("Cache Info")
        print("------------------")
        print("Cache capacity: {}".format(self.capacity))
        print("------------------")
        print("Address format ")
        print("|  tag:{}  |  indexSize:{}  |  offset:{}  |".format(self.tagSize, self.indexSize, self.offset))
        print("------------------")

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
