import accesspattern as AP
import nomocache as NOMO
import cache as PLAIN
import simulator as SIM
import dypacache as DYPA

# purpose of hit rate test
# compare hit rate of place cache and nomo cache
# show that both are similar

testCount = 50000
branch_prob = 0.3
loop_prob = 0.4
loop_mean = 8
loop_count = 128
sizeBit = 10
offset = 6
epoch = 5

def run(log, degree):
    # make plain and nomo cache
    plain_cache = PLAIN.FullyAssocCache(sizeBit, offset)
    nomo_cache = NOMO.NomoFullassocCache(sizeBit, offset, degree) 
    dypa_cache = DYPA.DypaFullassocCache(sizeBit,offset, degree)
    
    # plain run
    pattern = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    pattern1 = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    plist0 = [x for x in pattern]
    plist1 = [x for x in pattern1]

    cold0, hit0, conf0, intf0, cap0, stat_list0 = SIM.simulate('plain_test', plain_cache, iter(plist0), iter(plist1))

    # nomo run
    pattern = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    pattern1 = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    plist0 = [x for x in pattern]
    plist1 = [x for x in pattern1]

    cold1, hit1, conf1, intf1, cap1, stat_list1 = SIM.simulate('nomo_test', nomo_cache, iter(plist0), iter(plist1))
    
    # dypa run
    pattern = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    pattern1 = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    plist0 = [x for x in pattern]
    plist1 = [x for x in pattern1]

    cold2, hit2, conf2, intf2, cap2, stat_list2 = SIM.simulate('dypa_test', dypa_cache, iter(plist0), iter(plist1))    

    # write log
    miss0 = cold0 + conf0 + intf0 + cap0
    miss1 = cold1 + conf1 + intf1 + cap1
    miss2 = cold2 + conf2 + intf2 + cap2
    tCount = testCount * 2
    log.write('plain, {}, {}, {}, {}, {}, {}, {}\n'.format(degree, tCount, hit0, miss0, intf0, hit0 / tCount, intf0 / miss0))  
    log.write('nomo, {}, {}, {}, {}, {}, {}, {}\n'.format(degree, tCount, hit1, miss1, intf1, hit1 / tCount, intf1 / miss1))
    log.write('dypa, {}, {}, {}, {}, {}, {}, {}\n'.format(degree, tCount, hit2, miss2, intf2, hit2 / tCount, intf2 / miss2))

def main():
    deg_list = [16, 32, 64, 128, 256]
    with open('log_hitrate_test.csv', 'w') as log:
        log.write('name, degree, tcount, hit, miss, interfere, hitrate, intfrate\n')
        for deg in deg_list:
            for i in range(epoch):
                run(log, deg)

main()
