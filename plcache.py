WORD_SIZE=32

# partition-locking fully associative cache
# Fully associative cache
# only uses two more bits: L and ID
class PLFullassocCache:
    def __init__(self, sizeBit, offset):
        self.sizeBit = sizeBit
        self.offset = offset
        self.tagSize = WORD_SIZE - offset - 2
        self.lines = 2 ** sizeBit
        self.capacity = (2 ** sizeBit) * (2 ** offset)
        self.time = 0
        self.array = [None] * self.lines

    def printInfo(self):
        print("Cache Info")
        print("------------------")
        print("Cache lines: {}".format(self.lines))
        print("Cache capacity: {}B".format(self.capacity))
        print("Address format......", end="")
        print("|L|ID|  tag:{}  |  offset:{} |".format(self.tagSize,  self.offset))
        print("------------------")

    def translateAddr(self, addr):
        # make use of binary string
        binStr = bin(addr).replace('0b', '').zfill(WORD_SIZE)
        tagStr = binStr[0 : self.tagSize]
        offsetStr = binStr[-self.offset : ]
        tag = int(tagStr, 2)
        offset = int(offsetStr, 2)
        return (tag, 0, offset)

    def accessAddr(self, addr):
        # update time first
        self.time += 1
        # parse addr
        tag, index, offset = self.translateAddr(addr)
        # lru variable
        lru_index = 0
        lru_time = float('inf')
        # iterate over all array
        for i in range(self.lines):
            # if none, put in there wirh cold miss
            if self.array[i] == None:
                self.array[i] = {'tag': tag, 'time': self.time}
                return 'coldmiss'
            # if not, check tag
            else:
                # same tag, update time and hit
                if tag == self.array[i]['tag']:
                    self.array[i]['time'] = self.time
                    return 'hit'
                # diff tag, update lru and continue search
                elif lru_time > self.array[i]['time']:
                    lru_index = i
                    lru_time = self.array[i]['time']
        # iterated over all array, need evict by lru
        self.array[lru_index] = {'tag':tag, 'time': self.time}
        return 'capacity' 


