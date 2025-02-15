# SRA

> ## Description
>
> I just recently learnt about the SRA public key cryptosystem... or wait, was it supposed to be RSA? Hmmm, I should probably check...
>
> ## Hints
>
> - (None)

## Solution

First, we must understand how RSA works. Specifically, the public information that is *typically* shown to the public. Normally, the values of `n`, the public key,  `e`, the public key exponent, and `c`, the ciphertext, are revealed to the public. But, in this case, the values of `d`, the private key, `e`, the public key exponent, and `c`, the ciphertext, are given to us. Hence, the problem is named SRA instead of RSA because of its weird characteristics.

Normally, it is almost impossible to crack RSA without the private key because it is slow to factorize `n`, but since we already have the private key, this is not needed. Instead, the piece of information that we are missing `n`, as we need to compute `c^d mod n` to decrypt the ciphertext.

In order to find `n`, we need to do some math in order to express `n` in terms of `e` and `d`, which are provided to us. Since `n` is `p*q`, and the totient is `(p-1)*(q-1)`, we can find `n` if we find the totient as well.

The private key, `d`, can be calculated as `e^-1 mod t`. Moving `e` to the other side, we have `e*d = 1 mod t`. Further isolating t, we have `e*d-1 = k*(p-1)*(q-1)`(I made the `t` into `(p-1)*(q-1)` to make understanding this better).

The concept for the code for this solution is that we can calculate `ed-1`, take all of the subsets of three factors, and test values to see if `p` and `q` work to decipher the text. We can also implement a function to test if the deciphered plaintext is actually valid or not. Let's take a deep dive into our code.

```python
from Crypto.Util.number import long_to_bytes
from itertools import combinations, chain
from string import ascii_letters, digits
from factordb.factordb import FactorDB
from multiset import *
from math import gcd
from pwn import *
```

From these lines, we import `long_to_bytes` so that we can convert big numbers back to plaintext, `combinations` and `chain` to calculate subsets, `ascii_letters` and `digits` to calculate valid byte arrays, `FactorDB` to factor large numbers from python, `multiset` in order to subtract lists from each other, and finally, `gcd`, in order to check of `p` and `q` are valid.

```python
def product_list(lst):
    return 1 if len(lst) == 0 else (lst[0] * product_list(lst[1:]))
```

This defines a function that we will use later on, that uses recursion to multiply together all the items in a list.

```python
def calculate(d, c):
    ed1 = 65537 * d - 1
    _ = input('Factor ' + str(ed1) + ' on factordb')
    f = FactorDB(ed1)
    f.connect()
    factors = f.get_factor_list()
```

The first part of this function calculates `ed-1`(which I've named ed1 to make remembering it easier), and factors it via factordb's python api. The reason that it tells the user to factor it manually is that so that the database indexes the number, removing the possibility that factoring the number returns nothing.

```python
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
```

The second half of this function is where all the calculation actually takes place. `list(set(list(chain.from_iterable(combinations(factors, r) for r in range(1, len(factors) + 1)))))` will find all the combinations of the factors of `k`. The next line multiplies all the factors together, creating `k`. Note that I have written `list(set(list(` so that any duplicates will be removed(since multiplying all the numbers together will get the same result). We do not want `k` to be too large, as `p` and `q` are `128-bit` primes, so we turn to the next iteration if `k` is greater than `100000`.

Next, `pq_factors` calculate the factors that have not already been taken by `k`. The next line initializes another for loop, finding more combinations of factors in `pq_factors`, and after that, calculates `p` and `q` based on those combinations. Then, we can eliminate `p` and `q` based on more factors, such as if `p` or `q` is too small or too big, or if they are not coprime.

If `p` and `q` passes all these tests, then we can calculate the desired plaintext. Then, it tests if the plaintext is valid and if the length is `16`. If all of these tests return `True`, then we can return the plaintext out of the function.

The result is printed to the user, and entering it into the terminal, we have our flag. Note: you may need to connect to the server multiple times because ed1 may not always be fully factored in factorDB. Or, you may need to manually calculate the factors using alpertron because it is not fully factored.

```bash
anger = 6852441030146009801630249711517081732694063237186412562673717247864063759801
envy = 76360196736301857393494672389528064333009317539034447450852449835966118183953
vainglory?
> cQBP8SYgMHbSWqB2
Conquered!
picoCTF{redacted}
```
