import nomocache as NOMO
import accesspattern as AP
import simulator as SIM

def main():
    testCount = 1000
    sizeBit = 10
    offset = 6
    nomo_4 = NOMO.NomoSetassocCache(2, 2, 6, 1) 
    nomo_32 = NOMO.NomoSetassocCache(6, 4, 6, 8) 
    pattern = AP.realistic_pattern(testCount)
    plist0 = [x for x in pattern]
    plist1 = plist0.copy()
    SIM.simulate("nomo_4", nomo_4, iter(plist0), iter(plist1))  
    #SIM.simulate("nomo_32", nomo_32, iter(plist0), iter(plist1)) 

main()
