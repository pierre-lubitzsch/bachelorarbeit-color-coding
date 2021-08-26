#include <vector>
#include <cstdio>
#include <cmath>
#include <cassert>
#include <numeric>
#include <algorithm>
#include <cinttypes>


using namespace std;


uint32_t h_alpha(uint32_t x, uint32_t k, uint32_t p, uint32_t n) {
    return ((k * x) % p) % (n * n);
}

uint32_t h_beta(uint32_t x, uint32_t kappa, uint32_t rho, uint32_t n) {
    return ((kappa * x) % rho) % n;
}

uint32_t h_i(uint32_t x, uint32_t k_i, uint32_t rho, uint32_t c_i) {
    return ((k_i * x) % rho) % (c_i * c_i);
}


vector<vector<uint32_t>> cartesian_product(vector<vector<uint32_t>> &v) {
    vector<vector<uint32_t>> res = {{}};

    for (vector<uint32_t> &vec : v) {
        vector<vector<uint32_t>> cur;
        for (vector<uint32_t> &x : res) {
            for (uint32_t y : vec) {
                cur.push_back(x);
                cur.back().push_back(y);
            }
        }
        res = move(cur);
    }

    return res;
}



void print_vector(vector<vector<uint32_t>> &v) {
    for (vector<uint32_t> &x : v) {
        for (uint32_t y : x) {
            printf("%u ", y);
        }
        printf("\n");
    }
}


vector<vector<vector<uint32_t>>> get_kperfect_hash_family(uint32_t m, uint32_t n) {
    vector<vector<vector<uint32_t>>> family;

    vector<bool> isprime(ceil(n * n * log(m)) + 1, true);
    for (uint32_t prime_it = 2; prime_it * prime_it <= ceil(n * n * log(m)); ++prime_it) {
        if (isprime[prime_it]) {
            for (uint32_t i = prime_it * prime_it; i <= ceil(n * n * log(m)); i += prime_it) {
                isprime[i] = false;
            }
        }
    }

    uint32_t rho = n * n + 1;
    while (rho < 2 * n * n && !isprime[rho]) {
        ++rho;
    }
    assert(isprime[rho]);

    vector<vector<uint32_t>> n_lists(n, vector<uint32_t>(n));
    for (vector<uint32_t> &v : n_lists) {
        iota(v.begin(), v.end(), 0);
    }
    vector<vector<uint32_t>> cartesian_product_n_lists = cartesian_product(n_lists);
    vector<vector<uint32_t>> cartesian_product_n_lists_sum_squared_le_3n;
    copy_if(cartesian_product_n_lists.begin(), cartesian_product_n_lists.end(), back_inserter(cartesian_product_n_lists_sum_squared_le_3n), [](vector<uint32_t> &A) {
        uint32_t sum = 0;
        uint32_t square_sum = 0;
        for (int a : A) {
            sum += a;
            square_sum += a * a;
        }

        return sum == A.size() && square_sum < 3 * A.size();
    });
    // we don't need cartesian_product_n_lists anymore after we got the filtered one
    cartesian_product_n_lists.clear();
    

    vector<vector<uint32_t>> rho_lists = vector<vector<uint32_t>>(n, vector<uint32_t>(rho));
    for (vector<uint32_t> &v : rho_lists) {
        iota(v.begin(), v.end(), 0);
    }
    vector<vector<uint32_t>> cartesian_product_rho_lists = cartesian_product(rho_lists);

    //printf("%llu\n%llu\n%llu\n", cartesian_product_n_lists.size(), cartesian_product_n_lists_sum_squared_le_3n.size(), cartesian_product_rho_lists.size());

    //print_vector(cartesian_product_n_lists);
    //print_vector(cartesian_product_rho_lists);
    //print_vector(cartesian_product_rho_lists);

    printf("max_k = %u\n", n * n - 1);
    for (uint32_t k = 1; k < n * n; ++k) {
        printf("k = %u\n", k);
        for (uint32_t p = k + 1; p < ceil(n * n * log(m)); ++p) {
            if (!isprime[p]) {
                continue;
            }

            for (uint32_t kappa = 1; kappa < rho; ++kappa) {
                for (vector<uint32_t> &K : cartesian_product_rho_lists) {
                    for (vector<uint32_t> &c : cartesian_product_n_lists_sum_squared_le_3n) {
                        vector<uint32_t> C(n);

                        for (uint32_t i = 1; i < n; ++i) {
                            C[i] = C[i - 1] + c[i - 1] * c[i - 1];
                        }

                        family.push_back({{k}, {p}, {kappa}, {rho}, K, c, C});
                        if (family.size() % 1'000'000 == 0) {
                            printf("family size = %llu\n", family.size());
                        }
                    }
                }
            }
        }
    }

    return family;
}



int main() {
    vector<vector<vector<uint32_t>>> chi = get_kperfect_hash_family(100, 3);
    printf("length of chi: %llu\n", chi.size());
    return 0;
}