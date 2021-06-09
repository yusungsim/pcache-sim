import accesspattern as AP
import cache as PLAIN
import simulator as SIM

testCount = 50000
branch_prob = 0.3
loop_prob = 0.4
loop_mean = 8
loop_count = 128
sizeBit = 10
offset = 6
epoch = 5

def run(log):
    # make a plain cache
    plain_cache =  PLAIN.FullyAssocCache(sizeBit, offset)

    # make uniform pattern
    uni_pattern0 = AP.uniform_access(testCount)
    uni_pattern1 = AP.uniform_access(testCount)

    cold, hit, conf, intf, cap, stat_list = SIM.simulate('uniform', plain_cache, uni_pattern0, uni_pattern1)  
    miss = cold + conf + intf + cap
    tCount = testCount * 2

    log.write('uniform, {}, {}, {}, {}, {}, {}\n'.format(tCount, hit, miss, intf, hit / tCount, intf / miss))  

    # make realistic pattern
    real_pattern0 = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)
    real_pattern1 = AP.realistic_pattern(testCount, branch_prob=branch_prob, loop_prob=loop_prob, loop_mean=loop_mean, loop_count=loop_count)

    plain_cache =  PLAIN.FullyAssocCache(sizeBit, offset)

    cold, hit, conf, intf, cap, stat_list = SIM.simulate('realistic', plain_cache, real_pattern0, real_pattern1)  
    miss = cold + conf + intf + cap
    tCount = testCount * 2

    log.write('real, {}, {}, {}, {}, {}, {}\n'.format(tCount, hit, miss, intf, hit / tCount, intf / miss))  

def main():
    with open('log_pattern_test.csv', 'w') as log:
        for _ in range(epoch):
            run(log)

main()
