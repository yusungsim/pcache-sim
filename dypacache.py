WORD_SIZE=32

# Dynamically partition adjusting cache - fully associative cache
# no need change in ISA
# assume 2 threads
class DypaFullassocCache:
    def __init__(self, sizeBit, offset, degree):
        self.sizeBit = sizeBit
        self.offset = offset
        self.degree = degree
        self.tagSize = WORD_SIZE - offset
        self.lines = 2 ** sizeBit
        # check condition for degree: maximumn half
        if self.degree * 2 > self.lines:
            raise Exception("too large degree")
        self.capacity = (2 ** sizeBit) * (2 ** offset)
        # actual states
        self.time = 0
        self.dynDeg = [self.degree, self.degree]
        self.shared = self.lines - 2 * self.degree
        self.dynCount = [0, 0]
        self.dynThres = 2 

        self.locked = [0, 0]
        self.la0 = [None] * self.lines
        self.la1 = [None] * self.lines
        self.lockedarray = [self.la0, self.la1]
        self.sharedarray = [None] * self.lines

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
        lru_locked = True
        lru_index = 0
        lru_time = float('inf')
        
        # 0. iterator over corresponding locked partition first
        for i in range(self.dynDeg[thd]):
            # empty locked line exist: just use it
            if self.lockedarray[thd][i] == None:
                # locked number should be less than degree
                assert(self.locked[thd] < self.dynDeg[thd])
                self.lockedarray[thd][i] = {'thd': thd, 'tag': tag, 'time': self.time}
                self.locked[thd] += 1
                self.dynCount[thd] = 0
                return 'coldmiss'
            # not empty: check tag
            elif tag == self.lockedarray[thd][i]['tag']:
                self.lockedarray[thd][i]['time'] = self.time
                self.dynCount[thd] = 0
                return 'hit'
            # note matched: record lru and continue 
            else:
                if lru_time > self.lockedarray[thd][i]['time']:
                    lru_locked = True
                    lru_index = i
                    lru_time = self.lockedarray[thd][i]['time']

        # not returned until this point: locked partition should be full and no hit found
        assert(self.locked[thd] == self.dynDeg[thd])

        # 1. then iterate over shared part
        for i in range(self.shared):
            # if none, put in there with cold miss
            if self.sharedarray[i] == None:
                self.sharedarray[i] = {'thd':thd, 'tag': tag, 'time': self.time}
                self.dynCount[thd] = 0
                return 'coldmiss'

            # if not, check tag
            else:
                # same tag and thd, update time and hit
                # here, thread comparison needed
                if tag == self.sharedarray[i]['tag'] and thd == self.sharedarray[i]['thd']:
                    self.sharedarray[i]['time'] = self.time
                    self.dynCount[thd] = 0
                    return 'hit'
                # diff tag, update lru and continue search
                elif lru_time > self.sharedarray[i]['time']:
                    lru_locked = False
                    lru_index = i
                    lru_time = self.sharedarray[i]['time']

        # not returned until this point: no match found in whole array, so eviction needed
        self.dynCount[thd] += 1
        # eviction-check
        # if index is locked partition: it's  thd's locked partition.
        # free to cchangei t.
        if lru_locked:
            self.lockedarray[thd][lru_index] = {'thd': thd, 'tag': tag, 'time': self.time}
            return 'capacity'
        
        # else, it's shared partition
        # interference must be considered
        else:
            old_thd = self.sharedarray[lru_index]['thd']
            # if dynCount over threshold, lock one line from shared array
            if self.dynCount[thd] >= self.dynThres and self.dynDeg[thd] < (self.lines // 2):
                self.sharedarray.pop(lru_index)
                self.sharedarray.append(None)
                self.lockedarray[thd].append({'thd': thd, 'tag': tag, 'time': self.time})
                self.locked[thd] += 1
                self.dynDeg[thd] += 1
                self.shared -= 1
                self.dynCount[thd] = 0
                print("locked for", thd)

            # else, just do same as before
            else:
                self.sharedarray[lru_index] = {'thd': thd, 'tag':tag, 'time': self.time}
            # return interfere or just
            if thd != old_thd:
                return 'capacity-interfere'
            else:
                return 'capacity'

