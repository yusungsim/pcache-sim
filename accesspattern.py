import random
WORD_SIZE = 32

# various helper functions that create instance of
# memory access pattern, which is list of WORD_SIZE bit numbers
# each are genertors, use for to iterate over

# uniform access to total range of address set
def uniform_access(count):
    for i in range(count):
        yield random.randint(0, 2**WORD_SIZE)

# sequential program pattern
def sequential_with_jump(count, forward_prob=0.1, backward_prob=0.1, forward_dist=2**8, backward_dist=2**8, stdvar=2**2, bb_size=7):
    # check validity of prob
    if forward_prob + backward_prob > 1:
        raise Exception("probability over 1")
    # start from addr 0
    cur_addr = 0b0
    thres_forward = forward_prob
    thres_backward = forward_prob + backward_prob
    # make number of addresses
    bb_counter = 0
    # will yield exactly count count of addr
    for i in range(count):
        # 0. later return the "current" addr
        addr_to_return = cur_addr
        # 1. if in "basic block" mode, just do sequential
        if bb_counter > 0:
            cur_addr += 4
            bb_counter -= 1
        # 2. if out of basic block range, pick a random number
        else:
            picker = random.random() # 0 <= x < 1
            # then branch
            if picker < thres_forward:
                # case 1. forward jump
                delta = random.normalvariate(forward_dist, stdvar)
                delta = int(delta)
                cur_addr += 4 * (delta + 1)
                bb_counter = bb_size
            elif thres_forward <= picker < thres_backward:
                # case 2. backward jump
                delta = random.normalvariate(backward_dist, stdvar)
                delta = int(delta)
                cur_addr += 4 * (-delta + 1)
                bb_counter = bb_size
            else:
                # case 3. sequential
                cur_addr += 4
        # mod needed
        if cur_addr < 0:
            cur_addr = 0
        cur_addr = cur_addr % (2 ** WORD_SIZE)
        # return the addr_to_return
        yield addr_to_return

# more realistic pattern with finite state machine
def realistic_pattern(count, branch_prob=0.1, branch_mean=16, branch_stdvar=1, loop_prob=0.1, loop_count=16, loop_mean=16, loop_stdvar=1, bb_size=8):
    # check validity of probability
    if branch_prob + loop_prob > 1:
        raise Exception("probability over 1")
    # start from addr 0
    cur_addr = 0b0000
    # probability thresholds
    thres_branch = branch_prob
    thres_loop = branch_prob + loop_prob
    # state variable
    state = 'seq'
    # basic block counter
    bb_counter = 0
    # loop state
    loop_count = 0
    loop_init = 0
    loop_edge = 0
    # yield exactly count addr
    for i in range(count):
        addr_to_return = cur_addr
        # sequential state
        if state == 'seq':
            # Case 0. in a basic block: just seq
            if bb_counter > 0:
                bb_counter -= 1
                cur_addr += 4
            # Case 1. end of basic block
            else:
                # 1. pick a next state among seq, branch, loop
                picker = random.random() # 0 <= x < 1

                # 2. next: branmch
                if picker < thres_branch:
                    # pick a offset
                    delta = random.normalvariate(branch_mean, branch_stdvar) 
                    delta = int(delta)
                    cur_addr += 4 * (delta + 1)  
                    bb_counter = bb_size

                # 3. next: loopp
                elif thres_branch <= picker < thres_loop:
                    # change state to loop
                    state = 'loop'
                    # pick delta and count
                    delta = random.normalvariate(loop_mean, loop_stdvar)  
                    count = random.normalvariate(loop_count, loop_stdvar)
                    delta = int(delta)
                    count = int(count)
                    # set loop variables
                    loop_count = count
                    loop_init = cur_addr
                    loop_edge = cur_addr + delta
                    # sequentially go, will be handled by loop state
                    cur_addr += 4

                # 4. next: seq
                else:
                    cur_addr += 4
                    # let bb_counter stay 0
                    bb_counter = 0

        # looping state
        if state == 'loop':
            # if loop_edge: decrease cound and goto init 
            # if loop count 0: change to seq
            if cur_addr == loop_edge:
                if loop_count == 0:
                    state = 'seq'
                    cur_addr += 4
                    bb_counter = bb_size
                else:
                    loop_count -= 1
                    cur_addr = loop_init
            # not edge: just add
            else:
                cur_addr += 4
        # mod needed
        cur_addr = cur_addr % (2 ** WORD_SIZE) 
        # fianlly yield
        yield addr_to_return

def main():
    print("accesspattern.py - test")
    print("======= Sequential_with_jump ======")
    seq_example = sequential_with_jump(100, 0.1, 0.1, 2**8, 2**4, 2**2, 7) 
    for addr in seq_example:
        print(addr)
#main()
