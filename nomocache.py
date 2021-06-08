WORD_SIZE=32

# NoMo fully associative cache
# no need change in ISA
# assume 2 threads
class NomoFullassocCache:
    def __init__(self, sizeBit, offset, degree):
        self.sizeBit = sizeBit
        self.offset = offset
        self.degree = degree
        self.tagSize = WORD_SIZE - offset
        self.lines = 2 ** sizeBit
        self.capacity = (2 ** sizeBit) * (2 ** offset)
        # actual states
        self.time = 0
        self.locked = [0, 0]
        self.array = [None] * self.lines

    def printInfo(self):
        print("Cache Info")
        print("------------------")
        print("Cache lines: {}".format(self.lines))
        print("Cache capacity: {}B".format(self.capacity))
        print("NoMo degree: {}".format(self.degree))
        print("Address format......", end="")
        print("|L|ID|  tag:{}  |  offset:{} |".format(self.tagSize, self.offset))
        print("------------------")

    # consider 2 more bits
    def translateAddr(self, addr):
        # make use of binary string
        binStr = bin(addr).replace('0b', '').zfill(WORD_SIZE)
        tagStr = binStr[:self.tagSize]
        offsetStr = binStr[-self.offset:]
        tag = int(tagStr, 2)
        offset = int(offsetStr, 2)
        return (tag, 0, offset)
    
    # Mosly same procedure for accessing,
    # but adding thread-compare 
    # and lock-check when evicting
    def accessAddr(self, thd, addr):
        # check thread number 0 or 1
        if thd != 0 and thd != 1:
            raise Exception("thd number out of range")

        # update time first
        self.time += 1

        # parse addr
        tag, index, offset = self.translateAddr(addr)

        # lru variable
        lru_index = 0
        lru_time = float('inf')
        
        # 0. iterator over corresponding locked partition first
        for i in range(thd * self.degree, (thd+1) * self.degree):
            # empty locked line exist: just use it
            if self.array[i] == None:
                # locked number should be less than degree
                assert(self.locked[thd] < self.degree)
                self.array[i] = {'thd': thd, 'tag': tag, 'time': self.time}
                self.locked[thd] += 1
                return 'coldmiss'
            # not empty: check tag
            elif tag == self.array[i]['tag']:
                self.array[i]['time'] = self.time
                return 'hit'
            # note matched: record lru and continue 
            else:
                if lru_time > self.array[i]['time']:
                    lru_index = i
                    lru_time = self.array[i]['time']

        # not returned until this point: locked partition should be full and no hit found
        assert(self.locked[thd] == self.degree)

        # 1. then iterate over shared part
        for i in range(2*self.degree, self.lines):
            # if none, put in there with cold miss
            if self.array[i] == None:
                self.array[i] = {'thd':thd, 'tag': tag, 'time': self.time}
                return 'coldmiss'

            # if not, check tag
            else:
                # same tag and thd, update time and hit
                # here, thread comparison needed
                if tag == self.array[i]['tag'] and thd == self.array[i]['thd']:
                    self.array[i]['time'] = self.time
                    return 'hit'
                # diff tag, update lru and continue search
                elif lru_time > self.array[i]['time']:
                    lru_index = i
                    lru_time = self.array[i]['time']

        # not returned until this point: no match found in whole array, so eviction needed
        # eviction-check
        # if index is locked partition: it's  thd's locked partition.
        # free to cchangei t.
        if thd * self.degree <= lru_index < (thd + 1) * self.degree:
            self.array[lru_index] = {'thd': thd, 'tag': tag, 'time': self.time}
            return 'capacity'
        
        # else, it's shared partition
        # interference must be considered
        else:
            old_thd = self.array[lru_index]['thd']
            self.array[lru_index] = {'thd': thd, 'tag':tag, 'time': self.time}
            if thd != old_thd:
                return 'capacity-interfere'
            else:
                return 'capacity'
