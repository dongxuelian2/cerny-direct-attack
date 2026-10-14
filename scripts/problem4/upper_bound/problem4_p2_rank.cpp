// Small independent graph controls for PROOF.md#problem4-q13-second-layer.
// Enumerate every nonisolated labeled support with at most four edges.
// These are graph checks, not an enumeration of automata.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <utility>
#include <vector>
using namespace std;
using Matrix = vector<vector<long long>>;

int integer_rank(Matrix a) {
  int r = 0;
  for (int c = 0; !a.empty() && c < int(a[0].size()); ++c) {
    int p = r;
    while (p < int(a.size()) && !a[p][c]) ++p;
    if (p == int(a.size())) continue;
    swap(a[r], a[p]);
    for (int i = r + 1; i < int(a.size()); ++i) {
      if (!a[i][c]) continue;
      long long g = gcd(a[r][c], a[i][c]);
      long long u = a[r][c] / g, v = a[i][c] / g;
      for (int j = c; j < int(a[i].size()); ++j)
        a[i][j] = u * a[i][j] - v * a[r][j];
      long long common = 0;
      for (long long x : a[i]) common = gcd(common, x);
      if (common) for (auto& x : a[i]) x /= common;
    }
    ++r;
  }
  return r;
}

constexpr long long prime = 65537;
long long power(long long x, long long k) {
  long long y = 1;
  for (; k; k >>= 1, x = x * x % prime)
    if (k & 1) y = y * x % prime;
  return y;
}
int modular_rank(Matrix a) {
  int r = 0;
  for (int c = 0; !a.empty() && c < int(a[0].size()); ++c) {
    int p = r;
    while (p < int(a.size()) && !a[p][c]) ++p;
    if (p == int(a.size())) continue;
    swap(a[r], a[p]);
    long long inv = power(a[r][c], prime - 2);
    for (auto& x : a[r]) x = x * inv % prime;
    for (int i = r + 1; i < int(a.size()); ++i) {
      long long factor = a[i][c];
      for (int j = c; j < int(a[i].size()); ++j)
        a[i][j] = (a[i][j] - factor * a[r][j] % prime + prime) % prime;
    }
    ++r;
  }
  return r;
}

struct Family { int tau, rank, count; };
Family inspect(int n, const vector<unsigned>& edges) {
  int alpha = -1;
  Matrix rows;
  for (unsigned mask = 0; mask < (1u << n); ++mask) {
    bool independent = true;
    for (auto e : edges) if ((mask & e) == e) independent = false;
    if (!independent) continue;
    int size = __builtin_popcount(mask);
    if (size < alpha) continue;
    if (size > alpha) { alpha = size; rows.clear(); }
    vector<long long> row;
    for (int v = 0; v < n; ++v) row.push_back((mask >> v) & 1u);
    rows.push_back(row);
  }
  int r = integer_rank(rows);
  // All minors have order <= 8; Hadamard gives |det| <= 8^4 < prime.
  assert(r == modular_rank(rows));
  return {n - alpha, r, int(rows.size())};
}

int main() {
  uint64_t generated = 0, supports = 0, tau3 = 0;
  for (int n = 2; n <= 8; ++n) {
    vector<unsigned> pairs, selected;
    for (int u = 0; u < n; ++u) for (int v = u + 1; v < n; ++v)
      pairs.push_back((1u << u) | (1u << v));
    auto visit = [&](auto&& self, int next, unsigned used) -> void {
      ++generated;
      if (used == (1u << n) - 1) {
        ++supports;
        auto f = inspect(n, selected);
        if (f.tau == 3) { ++tau3; assert(f.rank <= 4); }
      }
      if (selected.size() == 4) return;
      for (int k = next; k < int(pairs.size()); ++k) {
        selected.push_back(pairs[k]);
        self(self, k + 1, used | pairs[k]);
        selected.pop_back();
      }
    };
    visit(visit, 0, 0);
  }
  auto matching = inspect(6, {3, 12, 48});
  auto triangle_edge = inspect(5, {3, 5, 6, 24});
  auto cycle = inspect(5, {3, 6, 12, 24, 17});
  assert(matching.tau == 3 && matching.rank == 4);
  assert(triangle_edge.tau == 3 && triangle_edge.rank == 4);
  assert(cycle.tau == 3 && cycle.rank == 5 && cycle.count == 5);
  assert(tau3 > 0);
  cout << "COMPLETE: " << generated << " labeled graphs with <=4 edges; "
       << supports << " nonisolated supports; " << tau3
       << " cover-three supports all have rank <=4.\n";
  cout << "PASS: integer/modular ranks agree; 3K2 and K3+K2 have rank 4; "
       << "C5 has rank 5 (the five-edge boundary cannot be included).\n";
  cout << "Scope: finite graph controls only; the uniform DFA argument is in PROOF.md.\n";
}
