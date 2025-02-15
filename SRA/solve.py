from Crypto.Util.number import long_to_bytes
from itertools import combinations, chain
from string import ascii_letters, digits
from factordb.factordb import FactorDB
from multiset import *
from math import gcd

def product_list(lst):
    return 1 if len(lst) == 0 else (lst[0] * product_list(lst[1:]))

def calculate(d, c):
    ed1 = 65537 * d - 1
    _ = input('Factor ' + str(ed1) + ' on factordb')
    f = FactorDB(ed1)
    f.connect()
    factors = f.get_factor_list()

    for k_factors in list(set(list(chain.from_iterable(combinations(factors, r) for r in range(1, len(factors) + 1))))):
        k = product_list(k_factors)
        if k > 100000:
            continue
        pq_factors = list(Multiset(factors) - Multiset(k_factors))
        for p_factors in list(set(list(chain.from_iterable(combinations(pq_factors, r) for r in range(1, len(pq_factors) + 1))))):
            p, q = product_list(p_factors) + 1, product_list(list(Multiset(pq_factors) - Multiset(p_factors))) + 1
            if p > 2**128 or p < 2**120 or q < 2**120 or q > 2**128 or gcd(p, q) != 1:
                continue
            plain = long_to_bytes(pow(c, d, p*q))
            if len(plain) != 16 or not all(byte in set([ord(c) for c in ascii_letters + digits]) for byte in plain):
                continue
            return plain

def main():
    c = int(input('c: '))
    d = int(input('d: '))
    print(calculate(d, c))

main()