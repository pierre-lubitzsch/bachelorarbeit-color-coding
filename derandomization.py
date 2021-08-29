import math
import numpy as np
import itertools


def h_alpha(x, k, p, n):
    return ((k * x) % p) % (n * n)

def h_beta(x, kappa, rho, n):
    return ((kappa * x) % rho) % n

def h_i(x, k_i, rho, c_i):
    return ((k_i * x) % rho) % (c_i * c_i) if c_i > 0 else 0


def sum_squared_le_3n(A):
    square_sum = 0
    for a in A:
        square_sum += a * a
    return square_sum < 3 * len(A) and sum(A) == len(A)


# m = number of elements in universe U = {0, 1, ..., m - 1}
# n = for all n-subsets A of U there exists a function f in the solution family such that A is perfectly hashed by f
def get_kperfect_hash_family(m, n):
    family = []

    # find a prime \rho > n^2 to use for h_{\beta}
    # we know that for all natural numbers x > 1 there always exists a prime between x and 2x by bertrand's postulate. Therefore 2n^2 is our upper bound for the sieve
    # use sieve of eratosthenes with upper bound and pick first prime larger than n * n
    isprime = [True for _ in range(2 * n * n)]
    prime_it = 2

    while (prime_it * prime_it < 2 * n * n):
        if (isprime[prime_it]):
            for i in range(prime_it * prime_it, 2 * n * n, prime_it):
                isprime[i] = False
        prime_it += 1
    
    rho = n * n + 1
    while (rho < 2 * n * n and not(isprime[rho])):
        rho += 1
    assert(isprime[rho])
    # now rho is the first prime number bigger than n^2


    n_lists = [list(range(n)) for _ in range(n)]
    cartesian_product_n_lists = list(itertools.product(*n_lists))
    # filter out lists where the condition for the hash function doesnt hold (condition: \sum c_i^2 <= 3n)
    cartesian_product_n_lists_sum_squared_le_3n = list(filter(sum_squared_le_3n, cartesian_product_n_lists))

    rho_lists = [list(range(rho)) for _ in range(n)]
    cartesian_product_rho_lists = list(itertools.product(*rho_lists))


    # testing
    print("max_k = ", n * n - 1)
    for k in range(1, n * n):
        print("k = ", k)
        for p in range(k + 1, math.ceil(n * n * np.log(m))):
            # above we calculated all primes below 2n^2, therefore we can skip numbers below 2n^2 if they are not marked as prime
            if (p < 2 * n * n and not(isprime[p])):
                continue

            # we have the function h_{\alpha}(x) = (kx mod p) mod n^2
            # now iterate over all possible h_{\beta} : h_{\alpha}(U) -> {0, 1, ..., n - 1}
            # for this we have already found a prime rho > n^2. now we try all possible values \kappa \in {0, ..., \rho - 1} for the function h_{\beta}(x) = (\kappa x mod \rho) mod n
            for kappa in range(1, rho):
                # now we need to choose the h_i where h_i(x) = (k_i * x mod rho) mod c_i^2, or in other words we need to choose the k_i
                # K is the table where K[i] = k_i
                # c is the table where c[i] = c_i
                # we iterate over all possibilities of K and c
                # therefore we take the cartesian product of n lists [0, 1, ..., n - 1] and filter out the good ones for c
                # we also take the cartesian product of n lists [0, 1, ..., rho - 1] for K
                
                for K in cartesian_product_rho_lists:
                    for c in cartesian_product_n_lists_sum_squared_le_3n:
                        # for little c, c[i] is the size of bucket i
                        # for big C, C[i] is the offset for storage of an element from bucket i in A*
                        C = [0] * n
                        for i in range(1, n):
                            C[i] = C[i - 1] + c[i - 1] * c[i - 1]

                        # up until now we got: k, p, kappa, rho, K[0 ... n - 1], c[0 ... n - 1], C[0 ... n - 1]
                        # with these we have a hash function because from n, k, p, kappa, rho we can construct h_alpha and h_beta and the h_i are defined by rho, K[i] and c[i]
                        # 
                        # the spaces to save values in the table of size 3n, aka the color/hash of the values in the other algorithm can be determined like this:
                        # for any element s of the universe U we calculate i = h_beta(h_alpha(s)) which is the bucket of the element (i \in {0, 1, ..., n - 1}).
                        # then we calculate the color/hash for s like this: C[i] + h_i(h_alpha(s)). this is without the compression table from {1, 2, ..., 3n} -> {1, 2, ..., n}.
                        # guessing the compression table would take time n^{3n}, because there are n^{3n} functions from {1, 2, ..., 3n} -> {1, 2, ..., n}.
                        family.append([k, p, kappa, rho, K, c, C])

    return family

chi = get_kperfect_hash_family(100, 3)
print(len(chi))












"""
# look at h_beta(h_alpha(U)) and construct secondary hash functions h_i
# c[i] contains all x \in universe U which are mapped to bucket i by (h_beta \circ h_alpha)
c = [[] for _ in range(n)]
for x in range(m):
    bucket_index = h_beta(h_alpha(x, k, p, n), kappa, rho, n)
    c[bucket_index].append(x)
"""
"""
DON'T USE, because this condition can only be checked for specific n-sets, we want to do it for all n-sets. just take all possibilities
# we can only use this kappa if \sum_{i = 0}^{n - 1} c[i]^2 < 3n (because only then we can store the function in a table of size 3n with the method we use)
sum_bucket_sizes_squared = 0
for i in range(n):
    sum_bucket_sizes_squared += len(c[i]) * len(c[i])
if (sum_bucket_sizes_squared >= 3 * n):
    continue
"""
"""
bucket_offset = [0] * n
for i in range(1, n):
    bucket_offset[i] = bucket_offset[i - 1] + len(c[i - 1]) * len(c[i - 1])
"""