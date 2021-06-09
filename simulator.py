import accesspattern as AP

WORD_SIZE=32

# simulate the cache pattern and print infos
# Total 2 threads, simulates to fairly schedule both threads and sharing cache
# returns stats on each thread's cache access,
# and also cache interference
# name: sring representing name of run
# cache : Cache class object
# pattern : iterator of WORD_SIZE ints, for each thread

def change_thd(cur_thd):
    return 0 if cur_thd == 1 else 1

def simulate(name, cache, pattern0, pattern1, quantum=1000):
    print("Run name:", name)
    filename = "log_" + name + ".txt"
    total_cold, total_hit, total_conflict, total_capacity = 0, 0, 0, 0
    cache.printInfo()

    # simulator considers thread running
    # running state variables
    cur_thd = 0
    cur_quantum = 0
    pattern_list = [pattern0, pattern1]
    stat_list = [{'cold':0, 'conflict':0, 'capacity': 0, 'readthru':0, 'hit': 0}, 
                {'cold':0, 'conflict':0, 'capacity': 0, 'readthru':0, 'hit': 0}]
    finished = [False, False]
    total_cold, total_conflict, total_capacity, total_interfere, total_hit = 0,0,0,0,0

    print("Run {} start...".format(name))
    with open(filename, 'w') as log:
        while True:
            # if both thread pattern finished, break
            if finished[0] and finished[1]:
                break
            # first, try getting next from iterator 
            try:
                addr = next(pattern_list[cur_thd])
            except StopIteration:
                # cur_thd finished.
                finished[cur_thd] = True
                # change cur_thd 
                cur_thd = change_thd(cur_thd)
                continue
                
            # access the address
            # TODO always lock the line change this
            result = cache.accessAddr(cur_thd, addr)
            # case by result
            if result == 'coldmiss':
                stat_list[cur_thd]['cold'] += 1
                total_cold += 1

            elif result == 'conflict':
                stat_list[cur_thd]['conflict'] += 1
                total_conflict += 1

            elif result == 'capacity':
                stat_list[cur_thd]['capacity'] += 1
                total_capacity += 1

            elif result == 'capacity-interfere':
                stat_list[cur_thd]['capacity'] += 1
                total_interfere += 1

            elif result == 'readthru':
                stat_list[cur_thd]['readthru'] += 1
                total_capacity += 1

            elif result == 'hit':
                stat_list[cur_thd]['hit'] += 1
                total_hit += 1

            log.write("thread {} access {} ({}), result: {}\n".format(cur_thd, addr, cache.translateAddr(addr), result))
            # update state
            cur_quantum += 1
            if cur_quantum >= quantum and not finished[change_thd(cur_thd)]:
                cur_thd = change_thd(cur_thd)
                cur_quantum = 0
 
    printResult(total_cold, total_hit, total_conflict, total_interfere, total_capacity, stat_list)
    return total_cold, total_hit, total_conflict, total_interfere, total_capacity, stat_list

def printResult(cold, hit, conflict, interfere, capacity, stat_list):
    total = cold + hit + conflict + capacity + interfere
    misses = cold + conflict + capacity + interfere

    print("-----------------------------")
    print("Total: {}".format(total))
    print("Hit: {}".format(hit))
    print("Miss: {} (cold: {}, conflict: {}, capacity: {}, interfere: {})".format(misses, cold, conflict, capacity, interfere))
    print("Hit rate:", hit / total)
    print("Interfere rate:", interfere / misses)
    print(stat_list)
    print("=================================================\n")
