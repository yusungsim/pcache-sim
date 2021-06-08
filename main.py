# Cache simulator
import accesspattern as AP
import simulator as SIM
import cache as CACHE
import plcache as PLC
import nomocache as NOMO

WORD_SIZE = 32

def main(testCount): 
    print("Test count: ", testCount)
    print("=========================================")
    
    # realistic test 
    # cache 64KB
    sizeBit = 10
    offset = 6
    nomo_0 = NOMO.NomoFullassocCache(sizeBit, offset, 0) 
    nomo_16 = NOMO.NomoFullassocCache(sizeBit, offset, 16) 
    nomo_32 = NOMO.NomoFullassocCache(sizeBit, offset, 32)  
    nomo_64 = NOMO.NomoFullassocCache(sizeBit, offset, 64) 
    # save pattern in list
    pattern = AP.realistic_pattern(testCount, branch_prob=0.3, loop_prob=0.4, loop_mean=8, loop_count=32)
    plist0 = [x for x in pattern]
    plist1 = plist0.copy() 

    #
    q = 100

    SIM.simulate("NomoFullassoc-0", nomo_0, iter(plist0), iter(plist1), q)
    print("=========================================")
    
    SIM.simulate("NomoFullassoc-16", nomo_16, iter(plist0), iter(plist1), q)
    print("=========================================")

    SIM.simulate("NomoFullassoc-32", nomo_32, iter(plist0), iter(plist1), q)
    print("=========================================")

    SIM.simulate("NomoFullassoc-64", nomo_64, iter(plist0), iter(plist1), q)
    print("=========================================")
main(10000)
