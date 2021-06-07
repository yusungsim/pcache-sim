import accesspattern as AP

WORD_SIZE=32

# simulate the cache pattern and print infos
# name: sring representing name of run
# cache : Cache class object
# pattern : iterator of WORD_SIZE length ints
def simulate(name, cache, pattern):
    filename = "log_" + name + ".txt"
    total_cold, total_hit, total_conflict, total_capacity = 0, 0, 0, 0
    print("Run {} start...".format(name))
    with open(filename, 'w') as log:
        for addr in pattern:
            result = cache.accessAddr(addr)
            if result == 'coldmiss':
                total_cold += 1
            elif result == 'conflict':
                total_conflict += 1
            elif result == 'capacity':
                total_capacity += 1
            elif result == 'hit':
                total_hit += 1
            log.write("access {} ({}), result: {}".format(addr, cache.translateAddr(addr), result)) 
    printResult(total_cold, total_hit, total_conflict, total_capacity)
    return total_cold, total_hit, total_conflict, total_capacity

def printResult(cold, hit, conflict, capacity):
    total = cold + hit + conflict + capacity
    misses = cold + conflict + capacity

    print("-----------------------------")
    print("Total: {}".format(total))
    print("Hit: {}".format(hit))
    print("Miss: {} (cold: {}, conflict: {}, capacity: {})".format(misses, cold, conflict, capacity))
    print("Hit rate:", hit / total)
    print("-----------------------------")
    
