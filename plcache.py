WORD_SIZE=32

# partition-locking fully associative cache
# Fully associative cache
# only uses two more bits: L and ID
class PLFullassocCache:
    def __init__(self, sizeBit, offset, lockCheck=True):
        self.sizeBit = sizeBit
        self.offset = offset
        self.lockCheck = lockCheck
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
        print("Checking lock: {}".format(self.lockCheck))
        print("Address format......", end="")
        print("|L|ID|  tag:{}  |  offset:{} |".format(self.tagSize,  self.offset))
        print("------------------")

    # consider 2 more bits
    def translateAddr(self, addr):
        # make use of binary string
        binStr = bin(addr).replace('0b', '').zfill(WORD_SIZE)
        tagStr = binStr[2 : 2+self.tagSize]
        offsetStr = binStr[-self.offset : ]
        tag = int(tagStr, 2)
        offset = int(offsetStr, 2)
        return (tag, 0, offset)
    
    # Mosly same procedure for accessing,
    # but adding thread-compare 
    # and lock-check when evicting
    def accessAddr(self, loc, thd, addr):
        # check thread number 0 or 1
        if thd != 0 and thd != 1:
            raise Exception("thd number out of range")
        # check loc 0 or 1
        if loc != 0 and loc != 1:
            raise Exception("loc out of range")

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
                self.array[i] = {'loc': loc, 'thd':thd, 'tag': tag, 'time': self.time}
                return 'coldmiss'
            # if not, check tag
            else:
                # same tag and thd, update time and hit
                if tag == self.array[i]['tag'] and thd == self.array[i]['thd']:
                    self.array[i]['time'] = self.time
                    return 'hit'
                # diff tag, update lru and continue search
                elif lru_time > self.array[i]['time']:
                    lru_index = i
                    lru_time = self.array[i]['time']
        # eviction-check: need consider loc
        # only do this when lockCheck on
        if self.lockCheck and self.array[lru_index]['loc'] == 1:
            # cannot evict, read main mem directly
            return 'readthru'
        else:
            old_thd = self.array[lru_index]['thd']
            # evict and replace
            self.array[lru_index] = {'loc':loc, 'thd':thd, 'tag':tag, 'time': self.time}
            # if thd was different from mine, result = interference
            if thd != old_thd:
                return 'capacity-interfere'
            else:
                return 'capacity' 


