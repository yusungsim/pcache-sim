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
            cur_addr += 2
            bb_counter -= 1
        # 2. if out of basic block range, pick a random number
        else:
            picker = random.random() # 0 <= x < 1
            # then branch
            if picker < thres_forward:
                # case 1. forward jump
                delta = random.normalvariate(forward_dist, stdvar)
                delta = int(delta)
                cur_addr += 2 * (delta + 1)
                bb_counter = bb_size
            elif thres_forward <= picker < thres_backward:
                # case 2. backward jump
                delta = random.normalvariate(backward_dist, stdvar)
                delta = int(delta)
                cur_addr += 2 * (-delta + 1)
                bb_counter = bb_size
            else:
                # case 3. sequential
                cur_addr += 2
        # mod needed
        if cur_addr < 0:
            cur_addr = 0
        cur_addr = cur_addr % (2 ** WORD_SIZE)
        # return the addr_to_return
        yield addr_to_return

def main():
    print("accesspattern.py - test")
    print("======= Sequential_with_jump ======")
    seq_example = sequential_with_jump(100, 0.1, 0.1, 2**8, 2**4, 2**2, 7) 
    for addr in seq_example:
        print(addr)
#main()
