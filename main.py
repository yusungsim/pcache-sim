# Cache simulator
import random
import accesspattern as AP
import simulator as SIM
import cache as CACHE

WORD_SIZE = 32

def main(testCount):
    seq_cache = CACHE.DirectMappedCache(16, 4)
    uni_cache = CACHE.DirectMappedCache(16, 4)
    seq_cache.printInfo()

    print("Test count: ", testCount)
    print("-----------------------------")
    
    # Sequential test
    seq_pattern = AP.sequential_with_jump(testCount, 0.05, 0.05, 2**8, 2**8, 2**2)
    SIM.simulate("Sequential", seq_cache, seq_pattern)
       
    # Uniform test 
    uni_pattern = AP.uniform_access(testCount)
    SIM.simulate("Uniform", uni_cache, uni_pattern)

main(1000000)
