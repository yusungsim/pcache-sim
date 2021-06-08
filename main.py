# Cache simulator
import accesspattern as AP
import simulator as SIM
import cache as CACHE
import plcache as PLC
import nomocache as NOMO

# 2-thread simulator for NoMoCache
# testCount: number of instr
# plist : list of pattern, WORD_SIZE bit numbers inside
# (generate this by accesspattern helpers
# (list will not be changed, will use iterator over it)
# degree: nomocache 
# q: quantum for context switching threads, default 100\
def testNomo(testCount, plist0, plist1, degree, q=100):
    print("Testing NoMoCache with degree: {}...".format(degree))
    print("-----------------------------------------")
    print("TestCount: {}".format(testCount))
    sizeBit = 10
    offset = 6
    nomo_cache = NOMO.NomoFullassocCache(sizeBit, offset, degree)
    
    result = SIM.simulate("NomoCache-"+str(degree), nomo_cache, iter(plist0), iter(plist1), q) 
    print("==============================================\n")
    return result

def main(testCount): 
    with open("log_test.txt", 'w') as log:
        # save pattern in list
        pattern = AP.realistic_pattern(testCount, branch_prob=0.3, loop_prob=0.4, loop_mean=8, loop_count=32)
        plist0 = [x for x in pattern]
        plist1 = plist0.copy() 

        deg_list = [8 * x for x in range(512//16)] 
        for deg in deg_list:
            cold, hit, conflict, interfere, capacity, stat_list = testNomo(testCount, plist0, plist1, deg, q=50)
            total = cold + hit + conflict + interfere + capacity
            misses = total - hit
            hit_rate = hit / total
            interfere_rate = interfere / misses
            log.write("Nomo-{} / HitRate {} / InterfereRate {}\n".format(deg, hit_rate, interfere_rate))

main(40000)
