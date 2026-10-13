// Complete support classification for the tau(P_6)=4, c(S)>=12 branch.
// Mathematical reduction to six/seven nonisolated vertices is in PROOF.md.
// This program classifies graphs only; it does not exclude their DFA actions.
// All arithmetic is exact: minors of independent-set rows have absolute
// determinant <= 3^(7/2) < 101, so rank over F_101 equals rank over Q.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <exception>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace {
using Row = std::array<int, 7>;
// Reference IDs are exactly those used by problem4_core_distances.cpp.
struct Reference { int n; const char* edges; };
constexpr Reference references[] = {
    {6,"01 04 05 12 15 23 25 34"},
    {6,"01 04 05 12 23 25 34 35 45"},
    {7,"01 04 12 23 34 56"},
    {7,"02 04 05 14 23 36 56"},
    {7,"01 06 12 23 34 45 56"},
    {7,"01 05 06 12 15 23 34 45"},
    {7,"04 12 15 23 24 36 45 56"},
    {7,"01 04 12 23 25 36 45 56"},
    {7,"01 04 12 15 23 34 35 45 56"}
};
struct Core {
    std::uint32_t mask;
    int rank;
    int maximum_sets;
    int pair_multiplicity;
};
struct Domain {
    int n;
    std::vector<std::pair<int, int>> edges;
    int index[7][7]{};
    explicit Domain(int size) : n(size) {
        for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j) {
            index[i][j] = index[j][i] = static_cast<int>(edges.size());
            edges.emplace_back(i, j);
        }
    }
    std::uint32_t count() const { return std::uint32_t{1} << edges.size(); }
};
int exact_rank(std::vector<Row> matrix, int n) {
    int rank = 0;
    for (int col = 0; col < n && rank < static_cast<int>(matrix.size()); ++col) {
        int pivot = rank;
        while (pivot < static_cast<int>(matrix.size()) && !matrix[pivot][col]) ++pivot;
        if (pivot == static_cast<int>(matrix.size())) continue;
        std::swap(matrix[pivot], matrix[rank]);
        int inverse = 1;
        while (inverse * matrix[rank][col] % 101 != 1) ++inverse;
        assert(inverse < 101);
        for (int j = col; j < n; ++j) matrix[rank][j] = matrix[rank][j] * inverse % 101;
        for (int i = rank + 1; i < static_cast<int>(matrix.size()); ++i) {
            const int scale = matrix[i][col];
            for (int j = col; j < n; ++j)
                matrix[i][j] = (matrix[i][j] - scale * matrix[rank][j] % 101 + 101) % 101;
        }
        ++rank;
    }
    return rank;
}
bool classify(const Domain& d, std::uint32_t mask, Core& result) {
    if (__builtin_popcount(mask) > 9) return false;
    std::array<unsigned, 7> adjacent{};
    std::array<int, 7> degree{};
    for (unsigned i = 0; i < d.edges.size(); ++i) if ((mask >> i) & 1U) {
        const auto [u, v] = d.edges[i];
        adjacent[u] |= 1U << v; adjacent[v] |= 1U << u;
        ++degree[u]; ++degree[v];
    }
    for (int i = 0; i < d.n; ++i) if (degree[i] == 0 || degree[i] > 4) return false;
    std::vector<Row> rows;
    unsigned covered = 0;
    const int alpha = d.n - 4;
    for (unsigned subset = 0; subset < (1U << d.n); ++subset) {
        const int size = __builtin_popcount(subset);
        if (size < alpha) continue;
        bool independent = true;
        for (int i = 0; i < d.n; ++i) if ((subset >> i) & 1U)
            if (adjacent[i] & subset) { independent = false; break; }
        if (!independent) continue;
        if (size > alpha) return false;
        Row row{};
        for (int i = 0; i < d.n; ++i) row[i] = (subset >> i) & 1U;
        rows.push_back(row); covered |= subset;
    }
    if (covered != (1U << d.n) - 1U) return false;
    const int rank = exact_rank(rows, d.n);
    if (rank < 6) return false;
    int pair_multiplicity = 0;
    for (int u = 0; u < d.n; ++u) for (int v = u + 1; v < d.n; ++v) {
        int count = 0;
        for (const Row& row : rows) count += row[u] && row[v];
        pair_multiplicity = std::max(pair_multiplicity, count);
    }
    // Checked for every survivor, never used as a pruning assumption.
    assert(pair_multiplicity <= 2);
    result = {mask, rank, static_cast<int>(rows.size()), pair_multiplicity};
    return true;
}
std::uint32_t make_mask(const Domain& d, std::initializer_list<std::pair<int,int>> pairs) {
    std::uint32_t mask = 0;
    for (auto [u,v] : pairs) mask |= 1U << d.index[u][v];
    return mask;
}
void controls() {
    Domain six(6), seven(7);
    Core result{};
    assert(!classify(six, 0, result));
    assert(!classify(seven, seven.count()-1, result));
    const auto cycle = make_mask(seven, {{0,1},{1,2},{2,3},{3,4},{4,5},{5,6},{6,0}});
    assert(classify(seven, cycle, result) && result.rank == 7 && result.maximum_sets == 7);
    const auto product = make_mask(seven, {{0,1},{1,2},{2,3},{3,4},{4,0},{5,6}});
    assert(classify(seven, product, result) && result.rank == 6 && result.maximum_sets == 10);
    // K_(3,3) has cover number three, outside this branch.
    const auto bipartite = make_mask(six, {{0,3},{0,4},{0,5},{1,3},{1,4},{1,5},{2,3},{2,4},{2,5}});
    assert(!classify(six, bipartite, result));
}
void run_domain(int n, unsigned threads) {
    const Domain domain(n);
    const std::uint32_t total = domain.count();
    std::vector<std::vector<Core>> output(threads);
    std::vector<std::exception_ptr> errors(threads);
    std::vector<std::thread> workers;
    // Half-open integer intervals partition every labeled graph mask exactly once.
    for (unsigned t = 0; t < threads; ++t) workers.emplace_back([&,t] {
        try {
            const auto begin = static_cast<std::uint32_t>(std::uint64_t(total) * t / threads);
            const auto end = static_cast<std::uint32_t>(std::uint64_t(total) * (t+1) / threads);
            for (std::uint32_t mask = begin; mask < end; ++mask) {
                Core core{};
                if (classify(domain, mask, core)) output[t].push_back(core);
            }
        } catch (...) { errors[t] = std::current_exception(); }
    });
    for (auto& worker : workers) worker.join();
    for (const auto& error : errors) if (error) std::rethrow_exception(error);
    std::vector<Core> survivors;
    for (auto& part : output) survivors.insert(survivors.end(), part.begin(), part.end());
    std::sort(survivors.begin(), survivors.end(), [](const Core& a,const Core& b){return a.mask<b.mask;});
    std::array<std::uint32_t,9> reference_masks{};
    std::array<bool,9> reference_covered{};
    for (int id=0;id<9;++id) if (references[id].n==n) {
        std::istringstream tokens(references[id].edges);
        std::string edge;
        while (tokens>>edge) {
            const int u=edge[0]-'0',v=edge[1]-'0';
            assert(edge.size()==2 && u>=0 && u<v && v<n);
            reference_masks[id] |= 1U<<domain.index[u][v];
        }
    }
    std::vector<unsigned char> seen(total);
    unsigned classes = 0;
    std::size_t orbit_sum = 0;
    for (const Core& core : survivors) {
        if (seen[core.mask]) continue;
        ++classes;
        std::array<int,7> permutation{};
        std::iota(permutation.begin(), permutation.begin()+n, 0);
        std::size_t orbit = 0;
        int reference_id = -1;
        do {
            std::uint32_t image = 0;
            for (unsigned i=0;i<domain.edges.size();++i) if ((core.mask>>i)&1U) {
                const auto [u,v] = domain.edges[i];
                image |= 1U << domain.index[permutation[u]][permutation[v]];
            }
            if (!seen[image]) { seen[image]=1; ++orbit; }
            for (int id=0;id<9;++id)
                if (references[id].n==n && image==reference_masks[id]) {
                    if (reference_id>=0 && reference_id!=id)
                        throw std::runtime_error("two distance reference IDs share one core orbit");
                    reference_id=id;
                }
        } while (std::next_permutation(permutation.begin(),permutation.begin()+n));
        if (reference_id<0)
            throw std::runtime_error("classified core orbit has no distance reference");
        if (reference_covered[reference_id])
            throw std::runtime_error("distance reference appears in multiple core orbits");
        reference_covered[reference_id]=true;
        orbit_sum += orbit;
        std::cout << "core="<<n<<" class="<<classes<<" reference_id="<<reference_id<<" rank="<<core.rank
                  <<" maximum_sets="<<core.maximum_sets<<" pair_multiplicity="<<core.pair_multiplicity<<" labeled_orbit="<<orbit<<" edges=";
        for (unsigned i=0;i<domain.edges.size();++i) if ((core.mask>>i)&1U)
            std::cout << domain.edges[i].first << domain.edges[i].second << ' ';
        std::cout << '\n';
    }
    assert(orbit_sum == survivors.size());
    for (int id=0;id<9;++id)
        if (references[id].n==n && !reference_covered[id])
            throw std::runtime_error("distance reference is not covered by classification");
    std::cout << "TOTAL core="<<n<<" examined="<<total<<" labeled_survivors="
              <<survivors.size()<<" classes="<<classes<<" reference_mapping=complete"<<'\n';
}
} // namespace
int main(int argc,char** argv) {
    try {
        unsigned threads = std::max(1U,std::min(64U,std::thread::hardware_concurrency()));
        for (int i=1;i<argc;++i) {
            const std::string argument=argv[i];
            if (argument=="--help") {
                std::cout<<"Usage: problem4_tau4_core [--threads 1..64]\n"; return 0;
            }
            if (argument!="--threads" || i+1==argc) throw std::invalid_argument("expected --threads 1..64");
            const std::string value=argv[++i];
            std::size_t consumed=0;
            const auto count=std::stoul(value,&consumed);
            if (consumed!=value.size() || count<1 || count>64) throw std::invalid_argument("threads must be 1..64");
            threads=static_cast<unsigned>(count);
        }
        controls();
        run_domain(6,threads); run_domain(7,threads);
    } catch (const std::exception& error) {
        std::cerr << "error: "<<error.what()<<'\n'; return 1;
    }
    return 0;
}
