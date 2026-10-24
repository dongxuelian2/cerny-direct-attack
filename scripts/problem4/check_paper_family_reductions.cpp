// Small complete transformation controls of local paper lemmas.
// No short-pair graph realization or global automaton exclusion is inferred.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
#ifdef NDEBUG
    std::cerr << "Assertions must be enabled.\n";
    return 1;
#endif
    for (int n : {6, 7}) {
        const unsigned all = (1u << n) - 1, J = all & ~63u;
        const unsigned TA = 7u | J, TB = 56u | J;
        const std::array<unsigned, 4> rows{TA & ~1u, TA & ~2u,
                                          TB & ~8u, TB & ~16u};
        long long total = 1, balanced = 0, clique = 0, permutations = 0;
        for (int i = 0; i < n; ++i) total *= n;
        for (long long code = 0; code < total; ++code) {
            std::array<int, 7> f{};
            auto value = code;
            unsigned output = 0;
            for (int i = 0; i < n; ++i) {
                f[i] = value % n;
                value /= n;
                output |= 1u << f[i];
            }
            auto image = [&](unsigned source) {
                unsigned result = 0;
                for (int i = 0; i < n; ++i)
                    if (source & (1u << i)) result |= 1u << f[i];
                return result;
            };
            auto count = [](unsigned x) { return __builtin_popcount(x); };
            const int rank = count(output);
            if (rank == n) ++permutations;
            // Balanced K_3,3: injective on each whole side plus J;
            // two different deletion rows per side remain independent.
            bool safe = count(image(TA)) == count(TA)
                     && count(image(TB)) == count(TB);
            for (unsigned row : rows) {
                unsigned target = image(row);
                safe = safe && !(target & 7u && target & 56u);
            }
            if (safe) {
                ++balanced;
                assert(rank == n || n - rank >= 3);
            }
            // Tight-layer clique-plus-edge: every kernel pair is an edge;
            // nonedge-to-edge images occupy at most one target edge.
            auto edge = [](int a, int b) {
                if (a == b) return false;
                return (a < 4 && b < 4) || (a == 4 && b == 5)
                     || (a == 5 && b == 4);
            };
            if (rank < n - 1) continue;
            bool compatible = true;
            unsigned terminal = 0;
            for (int a = 0; a < n; ++a) {
                for (int b = a + 1; b < n; ++b) {
                    if (edge(a, b)) continue;
                    if (f[a] == f[b]) compatible = false;
                    if (edge(f[a], f[b])) {
                        unsigned pair = (1u << f[a]) | (1u << f[b]);
                        if (terminal && terminal != pair) compatible = false;
                        terminal = pair;
                    }
                }
            }
            if (compatible) {
                ++clique;
                for (int i = 4; i < n; ++i) assert(f[i] >= 4);
            }
        }
        assert(balanced > 0 && clique > 0 && permutations > 0);
        std::cout << "PASS complete local maps: n=" << n << " maps=" << total
                  << " balanced_safe=" << balanced << " clique_compatible="
                  << clique << " permutations=" << permutations << '\n';
    }
}
