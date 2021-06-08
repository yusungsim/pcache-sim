# Cache simulator
import accesspattern as AP
import simulator as SIM
import cache as CACHE

WORD_SIZE = 32

def main(testCount): 
    print("Test count: ", testCount)
    print("=========================================")
     
    '''
    seq_cache = CACHE.DirectMappedCache(10, 6)
    uni_cache = CACHE.DirectMappedCache(10, 6)
    
    # Sequential test
    seq_pattern = AP.sequential_with_jump(testCount, 0.05, 0.05, 2**8, 2**8, 2**2)
    SIM.simulate("Sequential", seq_cache, seq_pattern)
    
    # Uniform test 
    uni_pattern = AP.uniform_access(testCount)
    SIM.simulate("Uniform", uni_cache, uni_pattern)
    ''' 

    # realistic test 
    real_cache = CACHE.DirectMappedCache(10, 6) 
    real_fullcache = CACHE.FullyAssocCache(10, 6)
    # save pattern in list
    real_pattern = AP.realistic_pattern(testCount, loop_prob=0.4, loop_mean=8, loop_count=32)
    real_list = [x for x in real_pattern]

    #
    SIM.simulate("DirectMapped", real_cache, real_list)
    print("=========================================")
    SIM.simulate("FullyAssociative",real_fullcache, real_list)
    print("=========================================")

main(100000)
