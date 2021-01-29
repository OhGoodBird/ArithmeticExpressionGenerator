#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random


OPERATOR = ['+', '-', '*', '/']


def check_parenthese_idx(left: list, right: list) -> bool:
    '''
    check parenthese is valid
    '''
    assert len(left) == len(right)
    for l, r in zip(left, right):
        if(l > r):
            return False
    return True


def generate_expression(config):
    # length >= 3 and should be odd number
    length = random.randint(3, config['max_length'])
    length = length + 1 if length % 2 != 1 else length

    # number of parentherse pair, i.e. ()
    num_parenthese_pair = random.randint(0, math.floor((length-1)/2))

    # generate number and operator list
    # e.g. ['2', '+', '3', '*', '4']
    seq = []
    for idx in range(length):
        if(idx % 2 == 0):
            n = random.randint(config['num_min'], config['num_max'])
            if(config['neg'] and random.randint(0, 2) == 0):
                n *= -1
                seq.append(f'({n})')
            else:
                seq.append(str(n))
        else:
            seq.append(OPERATOR[random.randint(0, len(OPERATOR)-1)])

    # insert parenthese into previous result list (seq)
    if(num_parenthese_pair):
        # find valid parenthese position
        pl = pr = num_parenthese_pair
        pl_possible_idx = [i for i in range(length) if i % 2 == 0]
        pr_possible_idx = [i for i in range(1, length+1) if i % 2 == 1]
        while(True):
            pl_idx = sorted(random.sample(pl_possible_idx, pl))
            pr_idx = sorted(random.sample(pr_possible_idx, pr))
            if(check_parenthese_idx(pl_idx, pr_idx)):
                break

        # intert '(', ')' character into result list
        seq_tmp = seq.copy()
        seq = []
        for idx in range(length):
            if(idx in pl_idx):
                seq.append('(')
                pl_idx.pop(0)
            elif(idx in pr_idx):
                seq.append(')')
                pr_idx.pop(0)
            seq.append(seq_tmp[idx])
        while(pr_idx):
            seq.append(')')
            pr_idx.pop(0)

    result = ' '.join(seq) if config['pretty'] else ''.join(seq)
    return result


def main():
    import sys
    import argparse
    try:
        from tqdm.auto import tqdm
    except:
        def tqdm(x, disable=False):
            return x
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', nargs='?', type=str,
                        default='stdout', help='output stream. (default=stdout)')
    parser.add_argument('-c', '--count', nargs='?', type=int,
                        default=10, help='how many arithmetic expression to generate.')
    parser.add_argument('-l', '--max_length', nargs='?', type=int, default=10,
                        help='max length of arithmetic expression. (default=10)')
    parser.add_argument('--max', nargs='?', type=int, default=10000,
                        help='absolute maximum value in arithmetic expression. (default=10000)')
    parser.add_argument('--min', nargs='?', type=int, default=0,
                        help='absolute minimum value in arithmetic expression. (default=0)')
    parser.add_argument('-n', '--allow-negative', action='store_true',
                        help='generate negative value or not. (default=False)')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='print pretty style expression string.')
    args = parser.parse_args()

    count = args.count
    config = {}
    max_length = args.max_length
    max_length = 3 if max_length < 3 else max_length
    config['max_length'] = max_length
    config['num_min'] = abs(args.min)
    config['num_max'] = abs(args.max)
    config['neg'] = args.allow_negative
    config['pretty'] = args.pretty

    if(args.output == 'stdout'):
        fp = sys.stdout
    elif(args.output == 'stderr'):
        fp = sys.stderr
    else:
        fp = open(args.output, 'w', encoding='utf8')

    for _ in tqdm(range(count), disable=fp in [sys.stdout, sys.stderr]):
        expression = generate_expression(config)
        print(f'{expression}', file=fp)


if __name__ == '__main__':
    main()
