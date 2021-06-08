# Cache simulator
import accesspattern as AP
import simulator as SIM
import cache as CACHE
import plcache as PLC

WORD_SIZE = 32

def main(testCount): 
    print("Test count: ", testCount)
    print("=========================================")
    
    # realistic test 
    # cache 64KB
    locked_cache = PLC.PLFullassocCache(12, 4, True) 
    unlocked_cache = PLC.PLFullassocCache(12, 4, False) 
    # save pattern in list
    pattern = AP.realistic_pattern(testCount, branch_prob=0.3, loop_prob=0.4, loop_mean=8, loop_count=32)
    plist1 = [x for x in pattern]
    plist2 = plist1.copy() 

    #
    q = 100

    SIM.simulate("PLFullassocUnlocked", unlocked_cache, iter(plist1), iter(plist2), q)
    print("=========================================")
    
    SIM.simulate("PLFullassocLocked", locked_cache, iter(plist1), iter(plist2), q)
    print("=========================================")

main(100000)
