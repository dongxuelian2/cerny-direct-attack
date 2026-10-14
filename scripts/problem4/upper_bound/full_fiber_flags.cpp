// Complete fiber-flag relaxation for the remaining (13,9,1) entrance cases.
// Mathematical scope and completeness: PROOF.md#problem4-full-fiber-flag.
// Exit 3 means relaxation survivors remain; it never certifies a DFA.
// Representatives model ONE letter; never iterate anonymous isolated labels.
// Direct input assignments are independently checked by kernel partitions
// with injective outputs, including triangles, flags, and arrow unions.
#include "short_word_alphabets.hpp"
#include <algorithm>
#include <array>
#include <atomic>
#include <cassert>
#include <cstdint>
#include <functional>
#include <iostream>
#include <map>
#include <mutex>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
using namespace std;
#ifndef FIBER_FLAG_STATES
#define FIBER_FLAG_STATES 13
#endif
constexpr int STATE_COUNT = FIBER_FLAG_STATES;
constexpr int SAFE_SIZE = STATE_COUNT - 4;
constexpr int SAFE_DEPTH = STATE_COUNT - 2;
constexpr int MASK_COUNT = 1 << STATE_COUNT;
static_assert(STATE_COUNT == 13 || STATE_COUNT == 14);

struct Core {
  int id, n;
  string text;
};
const vector<Core> cores = {
    {3, 4, "01 02 13"},          {4, 4, "01 02 13 23"},
    {6, 5, "01 02 03 14"},       {7, 5, "01 02 03 14 24"},
    {8, 5, "01 02 03 14 24 34"}, {9, 5, "01 02 13 24"},
    {10, 5, "01 02 34"},         {11, 6, "01 02 03 14 15"},
    {12, 6, "01 02 34 35"}};
struct Action {
  vector<int> pair;
  unsigned forced = 0, not_one = 0;
  bool operator<(const Action &b) const {
    return pair != b.pair
               ? pair < b.pair
               : (forced != b.forced ? forced < b.forced : not_one < b.not_one);
  }
};
// Distances only on the explicit P3 edges. An image outside P3 cannot
// supply a length <=3, so it has no arc in this reverse BFS.
vector<int> pair_bfs(int count, const vector<Action> &actions,
                     const vector<int> &pool) {
  vector<vector<int>> reverse(count);
  vector<int> distance(count, 99);
  queue<int> todo;
  for (int j : pool)
    for (int u = 0; u < count; ++u) {
      int v = actions[j].pair[u];
      if (v == -1 && distance[u] != 1) {
        distance[u] = 1;
        todo.push(u);
      } else if (v >= 0)
        reverse[v].push_back(u);
    }
  while (!todo.empty()) {
    int v = todo.front();
    todo.pop();
    for (int u : reverse[v])
      if (distance[u] > distance[v] + 1) {
        distance[u] = distance[v] + 1;
        todo.push(u);
      }
  }
  return distance;
}
struct Mark {
  array<unsigned, STATE_COUNT + 1> arrows{};
  unsigned flags = 0;
};
struct Case {
  Core core;
  int B, C, D, E, F, G, H, I, J, K, L;
  int fixed() const {
    return max(core.n + 1, 32 - __builtin_clz(unsigned(B | C | D | E | F | G |
                                                       H | I | J | K | L)));
  }
  int qj() const { return min(fixed(), STATE_COUNT - 1); }
  int depth() const {
    return L ? 11
             : (K ? 10
                  : (J ? 9
                       : (I ? 8 : (H ? 7 : (G ? 6 : (F ? 5 : (E ? 4 : 3)))))));
  }
  int fiber_at(int i) const {
    return array<int, 12>{1 << core.n, B, C, D, E, F, G, H, I, J, K, L}.at(i);
  }
  vector<int> &closure(int i) { return higher_fibers.at(i); }
  const vector<int> &closure(int i) const { return higher_fibers.at(i); }
  int limit = 11;
  array<vector<int>, 12> higher_fibers;
  set<int> extensions;
  vector<vector<int>> raw_maps;
  vector<Action> raw_profiles;
  vector<pair<int, int>> edges, long_pairs;
  vector<int> all_third;
  vector<int> fibers;
  int index[STATE_COUNT + 1][STATE_COUNT + 1];
  vector<Action> actions;
  vector<Mark> marks;
  uint64_t domains = 0, signature_count = 0, joint = 0, sc = 0,
           kernel_domains = 0;
  vector<vector<int>> survivor_vectors;
  uint64_t invalid_p1 = 0;
  mutable map<pair<int, int>, pair<vector<unsigned>, array<bool, MASK_COUNT>>>
      family_cache;

  Case(Core h, int b, int c, int d, int e = 0, int f = 0, int g = 0, int hh = 0,
       int ii = 0, int jj = 0, int kk = 0, int ll = 0)
      : core(h), B(b), C(c), D(d), E(e), F(f), G(g), H(hh), I(ii), J(jj), K(kk),
        L(ll) {
    for (auto &row : index)
      fill(begin(row), end(row), -2);
    istringstream input(core.text);
    string text;
    while (input >> text) {
      int u = text[0] - '0', v = text[1] - '0';
      index[u][v] = index[v][u] = edges.size();
      edges.push_back({u, v});
    }
  }
  bool cover_three(const vector<int> &cliques) const {
    auto cover = [&](auto &&self, unsigned selected, int left) -> bool {
      for (int clique : cliques) {
        unsigned rest = unsigned(clique) & ~selected;
        if (__builtin_popcount(rest) <= 1)
          continue;
        if (!left)
          return false;
        unsigned u = rest & -rest;
        rest ^= u;
        unsigned v = rest & -rest;
        return self(self, selected | u, left - 1) ||
               self(self, selected | v, left - 1);
      }
      return true;
    };
    return cover(cover, 0, 3);
  }
  vector<int> known_p6() const {
    vector<int> cliques;
    for (auto [u, v] : edges)
      cliques.push_back((1 << u) | (1 << v));
    for (int i = 1; i <= min(depth(), 6); ++i)
      cliques.push_back(fiber_at(i));
    return cliques;
  }
  bool letter_p6(const vector<int> &f) const {
    auto cliques = known_p6();
    auto pre = [&](int mask) {
      int out = 0;
      for (int q = 0; q < int(f.size()); ++q)
        if (mask >> f[q] & 1)
          out |= 1 << q;
      return out;
    };
    for (auto [u, v] : edges)
      cliques.push_back(pre((1 << u) | (1 << v)));
    for (int i = 1; i <= min(depth(), 5); ++i)
      cliques.push_back(pre(fiber_at(i)));
    return cover_three(cliques);
  }
  bool prepare() {
    if (!cover_three(known_p6()))
      return false;
    // V_(SAFE_DEPTH-k) has dimension STATE_COUNT-1-k and annihilator H_k. The complete
    // literal family contains all these actual short images. Its row space
    // is exactly that trajectory space when the ranks agree, so a Boolean mask is a
    // one-count fiber in H_k iff it meets every member in exactly one point.
    vector<int> identity(STATE_COUNT);
    iota(identity.begin(), identity.end(), 0);
    for (int level = 3; level <= depth(); ++level) {
      vector<unsigned> family;
      unsigned covered = 0;
      bool alone[STATE_COUNT][STATE_COUNT]{};
      for (unsigned mask = 0; mask < (1U << STATE_COUNT); ++mask) {
        if (__builtin_popcount(mask) != SAFE_SIZE || !(mask >> core.n & 1))
          continue;
        bool valid = true;
        for (int i = 1; i <= level; ++i)
          if (__builtin_popcount(mask & unsigned(fiber_at(i))) != 1)
            valid = false;
        for (auto [u, v] : edges)
          if ((mask >> u & 1) && (mask >> v & 1))
            valid = false;
        if (!valid)
          continue;
        family.push_back(mask);
        covered |= mask;
        for (int u = 0; u < STATE_COUNT; ++u)
          if (mask >> u & 1)
            for (int v = 0; v < STATE_COUNT; ++v)
              if (!(mask >> v & 1))
                alone[u][v] = true;
      }
      if (level <= 7 && covered != (1U << STATE_COUNT) - 1)
        return false;
      int need = STATE_COUNT - 1 - level;
      for (int threshold : {need, need + 1}) {
        bool rank = safe_rank(identity, SAFE_SIZE, threshold, false, level);
        assert(rank == safe_rank(identity, SAFE_SIZE, threshold, true, level));
        if (rank != (threshold == need))
          return false;
      }
      vector<int> &candidates = level == 3 ? all_third : closure(level);
      for (unsigned mask = 1; mask < (1U << STATE_COUNT); ++mask) {
        bool valid = true;
        for (unsigned set : family)
          if (__builtin_popcount(mask & set) != 1) {
            valid = false;
            break;
          }
        if (valid)
          candidates.push_back(mask);
      }
      if (level == 3)
        for (int mask : candidates) {
          bool clique = true;
          for (int u = 0; u < STATE_COUNT; ++u)
            for (int v = u + 1; v < STATE_COUNT; ++v)
              if ((mask >> u & 1) && (mask >> v & 1) && index[u][v] < 0)
                clique = false;
          if (clique)
            fibers.push_back(mask);
        }
      // Arrival within four steps applies through flag seven. In particular
      // an implication u in T => v in T certifies co-occurrence in an actual
      // short image; the relaxed family need not itself be reachable.
      if (level <= 7)
        for (int u = 0; u < STATE_COUNT; ++u)
          for (int v = u + 1; v < STATE_COUNT; ++v)
            if (!alone[u][v] || !alone[v][u])
              long_pairs.push_back({u, v});
      if (level <= 7)
        for (int mask : candidates)
          if (__builtin_popcount(unsigned(mask)) == 2) {
            int u = __builtin_ctz(unsigned(mask)),
                v = __builtin_ctz(unsigned(mask & ~(1 << u)));
            for (int z = 0; z < core.n; ++z)
              if (z != u && z != v) {
                if (index[u][z] >= 0)
                  long_pairs.push_back(minmax(v, z));
                if (index[v][z] >= 0)
                  long_pairs.push_back(minmax(u, z));
              }
          }
    }
    sort(long_pairs.begin(), long_pairs.end());
    long_pairs.erase(unique(long_pairs.begin(), long_pairs.end()),
                     long_pairs.end());
    for (auto [u, v] : long_pairs)
      if (index[u][v] >= 0)
        return false;
    return find(fibers.begin(), fibers.end(), D) != fibers.end();
  }
  int target(int u, int v) const { return u == v ? -1 : index[u][v]; }
  bool mandatory(int u) const {
    for (int i = 0; i <= min(depth(), 7); ++i)
      if (fiber_at(i) == (1 << u))
        return true;
    return false;
  }
  bool safe_rank(const vector<int> &f, int size, int need, bool exact = false,
                 int level = 3) const {
    // Independent relabelings of anonymous inputs/outputs preserve these full
    // subset families, so the omitted bijection can be the identity here.
    if (need <= 0)
      return true;
    array<array<long long, STATE_COUNT>, STATE_COUNT> integer_basis{};
    constexpr int P = 65521;
    array<array<int, STATE_COUNT>, STATE_COUNT> basis{};
    int rank = 0;
    auto power = [](int a, int b) {
      int z = 1;
      while (b) {
        if (b & 1)
          z = int(1LL * z * a % P);
        a = int(1LL * a * a % P);
        b >>= 1;
      }
      return z;
    };
    auto family = [&](unsigned mask) {
      for (auto [u, v] : edges)
        if ((mask >> u & 1) && (mask >> v & 1))
          return false;
      if (size == SAFE_SIZE) {
        if (!(mask >> core.n & 1))
          return false;
        for (int i = 1; i <= level; ++i)
          if (__builtin_popcount(mask & unsigned(fiber_at(i))) != 1)
            return false;
      }
      return true;
    };
    auto key = make_pair(size, level);
    auto it = family_cache.find(key);
    if (it == family_cache.end()) {
      pair<vector<unsigned>, array<bool, MASK_COUNT>> entry{};
      for (unsigned mask = 0; mask < (1U << STATE_COUNT); ++mask)
        if (__builtin_popcount(mask) == size && family(mask)) {
          entry.first.push_back(mask);
          entry.second[mask] = true;
        }
      it = family_cache.emplace(key, move(entry)).first;
    }
    for (unsigned mask : it->second.first) {
      unsigned out = 0;
      for (int q = 0; q < STATE_COUNT; ++q)
        if (mask >> q & 1)
          out |= 1U << (q < int(f.size()) ? f[q] : q);
      if (!it->second.second[out])
        continue;
      if (exact) {
        array<long long, STATE_COUNT> row{};
        for (int q = 0; q < STATE_COUNT; ++q)
          row[q] = mask >> q & 1;
        for (int q = 0; q < STATE_COUNT; ++q)
          if (row[q]) {
            if (!integer_basis[q][q]) {
              integer_basis[q] = row;
              if (++rank >= need)
                return true;
              break;
            }
            long long a = integer_basis[q][q], b = row[q], g = 0;
            for (int j = q; j < STATE_COUNT; ++j) {
              row[j] = a * row[j] - b * integer_basis[q][j];
              g = gcd(g, abs(row[j]));
            }
            if (g)
              for (int j = q; j < STATE_COUNT; ++j)
                row[j] /= g;
          }
        continue;
      }
      array<int, STATE_COUNT> row{};
      for (int q = 0; q < STATE_COUNT; ++q)
        row[q] = mask >> q & 1;
      for (int q = 0; q < STATE_COUNT; ++q)
        if (row[q]) {
          if (!basis[q][q]) {
            int inv = power(row[q], P - 2);
            for (int j = q; j < STATE_COUNT; ++j)
              basis[q][j] = int(1LL * row[j] * inv % P);
            if (++rank >= need)
              return true;
            break;
          }
          int t = row[q];
          for (int j = q; j < STATE_COUNT; ++j)
            row[j] = int((row[j] - 1LL * t * basis[q][j] % P + P) % P);
        }
    }
    return false;
  }
  bool partial_flags(const vector<int> &f) const {
    unsigned assigned = 0;
    for (int q = 0; q < int(f.size()); ++q)
      if (f[q] >= 0)
        assigned |= 1U << q;
    for (int level = 4; level <= depth(); ++level) {
      unsigned before = 0;
      for (int q = 0; q < int(f.size()); ++q)
        if (f[q] >= 0 && (fiber_at(level - 1) >> f[q] & 1))
          before |= 1U << q;
      bool possible = false;
      for (int candidate : closure(level))
        if (!(unsigned(candidate) >> f.size()) &&
            (unsigned(candidate) & assigned) == before) {
          possible = true;
          break;
        }
      if (!possible)
        return false;
    }
    return true;
  }
  bool forced_images(const vector<int> &f) const {
    // If the full literal family has exactly its required rank many rows,
    // every row must occur in the actual short orbit that spans this space.
    for (int level = 4; level <= depth(); ++level) {
      const auto &family = family_cache.at({SAFE_SIZE, level}).first;
      if (int(family.size()) != STATE_COUNT - 1 - level)
        continue;
      for (unsigned mask : family) {
        for (int steps = 1; steps <= (fixed() >= STATE_COUNT - 1 ? level : 1); ++steps) {
          unsigned out = 0;
          for (int q = 0; q < STATE_COUNT; ++q)
            if (mask >> q & 1)
              out |= 1U << (q < int(f.size()) ? f[q] : q);
          if (__builtin_popcount(out) != SAFE_SIZE || !(out >> core.n & 1))
            return false;
          if (level - steps >= 3 &&
              !family_cache.at({SAFE_SIZE, level - steps}).second[out])
            return false;
          mask = out;
        }
      }
    }
    return true;
  }
  bool fourth_allowed(const vector<int> &f) const {
    if (!forced_images(f))
      return false;
    if (!letter_p6(f))
      return false;
    if (!E)
      return true;
    int pre = 0;
    for (int q = 0; q < int(f.size()); ++q)
      if (D >> f[q] & 1)
        pre |= 1 << q;
    if (find(closure(4).begin(), closure(4).end(), pre) == closure(4).end())
      return false;
    for (int level = 5; level <= depth(); ++level) {
      int preE = 0;
      for (int q = 0; q < int(f.size()); ++q)
        if (fiber_at(level - 1) >> f[q] & 1)
          preE |= 1 << q;
      const auto &family = closure(level);
      if (find(family.begin(), family.end(), preE) == family.end())
        return false;
    }
    // At depth seven the next preimages are one-count only through depth
    // three; four-step arrival no longer justifies the antichain pruning.
    if (depth() >= 7)
      return true;
    const auto &bool_fibers = closure(depth());
    for (int fiber : bool_fibers) {
      unsigned before = 0;
      for (int q = 0; q < int(f.size()); ++q)
        if (fiber >> f[q] & 1)
          before |= 1U << q;
      if (!before)
        return false;
      if (__builtin_popcount(before) == 1 && __builtin_ctz(before) < core.n)
        return false;
      for (int old : bool_fibers)
        if (before != unsigned(old) &&
            ((before & old) == before || (before & old) == unsigned(old)))
          return false;
      bool actual = false;
      for (int i = 0; i <= depth(); ++i)
        actual |= (fiber == fiber_at(i));
      if (actual)
        for (auto [u, v] : long_pairs)
          if ((before >> u & 1) && (before >> v & 1))
            return false;
      if (__builtin_popcount(before) == 2) {
        int u = __builtin_ctz(before), v = __builtin_ctz(before & ~(1U << u));
        for (int z = 0; z < core.n; ++z)
          if (index[u][z] >= 0 && index[v][z] >= 0)
            return false;
      }
    }
    return true;
  }
  vector<int> canonical_map(vector<int> f) const {
    // Anonymous inputs are sorted by their distinct explicit outputs.
    // Normalize anonymous outputs by first occurrence in literal input order.
    vector<int> relabel(f.size(), -1);
    int next = fixed();
    for (int &output : f)
      if (output >= fixed()) {
        if (relabel[output] < 0)
          relabel[output] = next++;
        output = relabel[output];
      }
    return f;
  }
  bool fresh_anonymous_output(int output, unsigned used) const {
    if (output < fixed() || (used >> output & 1))
      return true;
    for (int earlier = fixed(); earlier < output; ++earlier)
      if (!(used >> earlier & 1))
        return false;
    return true;
  }
  bool sorted_anonymous_input(int input, int output,
                              const vector<int> &f) const {
    if (input < fixed())
      return true;
    for (int q = fixed(); q < int(f.size()); ++q)
      if (q != input && f[q] >= 0)
        if ((q < input && f[q] >= output) || (q > input && f[q] <= output))
          return false;
    return true;
  }
  void power_edges(const vector<int> &f, Action &action) const {
    if (fixed() < STATE_COUNT - 1)
      return;
    for (int level = 4; level <= depth(); ++level) {
      const auto &family = family_cache.at({SAFE_SIZE, level}).first;
      if (int(family.size()) != STATE_COUNT - 1 - level)
        continue;
      for (unsigned mask : family)
        for (int step = 1; step < level; ++step) {
          unsigned out = 0;
          for (int q = 0; q < STATE_COUNT; ++q)
            if (mask >> q & 1)
              out |= 1U << (q < int(f.size()) ? f[q] : q);
          mask = out;
          int remaining = level - step;
          if (remaining > 2)
            continue;
          for (size_t i = 0; i < edges.size(); ++i) {
            auto [u, v] = edges[i];
            if ((mask >> u & 1) && (mask >> v & 1)) {
              if (remaining == 2)
                action.forced |= 1U << i;
              else
                action.not_one |= 1U << i;
            }
          }
        }
    }
  }
  void generate() {
    int n = core.n;
    map<Action, Mark> signatures;
    for (int k = 0; k <= min(fixed() - 1 - __builtin_popcount(unsigned(B | C)),
                             STATE_COUNT - fixed());
         ++k) {
      int N = fixed() + k;
      vector<int> f(N, -1);
      for (int preA : {1 << n, B})
        for (int preB : {1 << n, B, C})
          for (int preC : fibers) {
            vector<vector<int>> allowed(N);
            for (int q = 0; q < N; ++q)
              for (int out = 0; out < N; ++out) {
                if (q >= fixed() &&
                    (out >= fixed() || out == n || ((B | C) >> out & 1)))
                  continue;
                if (bool(preA >> q & 1) != (out == n))
                  continue;
                if (bool(preB >> q & 1) != bool(B >> out & 1))
                  continue;
                if (bool(preC >> q & 1) != bool(C >> out & 1))
                  continue;
                allowed[q].push_back(out);
              }
            vector<int> order(N);
            iota(order.begin(), order.end(), 0);
            stable_sort(order.begin(), order.end(), [&](int u, int v) {
              return allowed[u].size() < allowed[v].size();
            });
            function<void(int, unsigned, int)> assign =
                [&](int at, unsigned outputs, int deficiency) {
                  if (at == N) {
                    assert(__builtin_popcount(outputs) >= N - 2);
                    if (!fourth_allowed(f))
                      return;
                    if (!safe_rank(f, STATE_COUNT - 3, 3) || !safe_rank(f, SAFE_SIZE, SAFE_DEPTH - 3))
                      return;
                    for (int level = 4; level <= depth(); ++level)
                      if (!safe_rank(f, SAFE_SIZE, SAFE_DEPTH - level, false, level))
                        return;
                    ++domains;
                    raw_maps.push_back(canonical_map(f));
                    Action action;
                    for (auto [u, v] : edges)
                      action.pair.push_back(target(f[u], f[v]));
                    for (int u = 0; u < N; ++u)
                      for (int v = u + 1; v < N; ++v)
                        if (index[u][v] < 0) {
                          int t = target(f[u], f[v]);
                          assert(t != -1);
                          if (t >= 0)
                            action.forced |= 1U << t;
                        }
                    power_edges(f, action);
                    Mark &mark = signatures[action];
                    for (int level = 5; level <= depth(); ++level) {
                      int pre = 0;
                      for (int q = 0; q < N; ++q)
                        if (fiber_at(level - 1) >> f[q] & 1)
                          pre |= 1 << q;
                      if (pre == fiber_at(level))
                        mark.flags |= 1U << (level - 1);
                    }
                    if (E) {
                      int pre = 0;
                      for (int q = 0; q < N; ++q)
                        if (D >> f[q] & 1)
                          pre |= 1 << q;
                      if (pre == E)
                        mark.flags |= 8;
                    }
                    mark.arrows[qj()] |= 1U << qj();
                    for (int q = 0; q < N; ++q)
                      mark.arrows[min(q, qj())] |= 1U << min(f[q], qj());
                    if (preA == B)
                      mark.flags |= 1;
                    if (preB == C)
                      mark.flags |= 2;
                    if (preC == D)
                      mark.flags |= 4;
                    return;
                  }
                  int q = order[at];
                  for (int out : allowed[q]) {
                    if (!fresh_anonymous_output(out, outputs) ||
                        !sorted_anonymous_input(q, out, f))
                      continue;
                    if (count(f.begin(), f.end(), out) >= 3)
                      continue;
                    int new_def = deficiency + bool(outputs >> out & 1);
                    if (new_def > 2)
                      continue;
                    bool ok = true;
                    for (int i = 0; i < at; ++i) {
                      int other = order[i];
                      if (f[other] == out && index[q][other] < 0)
                        ok = false;
                      bool long_pair =
                          mandatory(q) || mandatory(other) ||
                          find(long_pairs.begin(), long_pairs.end(),
                               make_pair(min(q, other), max(q, other))) !=
                              long_pairs.end();
                      if (long_pair && target(out, f[other]) >= -1)
                        ok = false;
                    }
                    if (!ok)
                      continue;
                    f[q] = out;
                    if (partial_flags(f))
                      assign(at + 1, outputs | (1U << out), new_def);
                    f[q] = -1;
                  }
                };
            assign(0, 0, 0);
          }
    }
    for (const auto &[action, mark] : signatures) {
      actions.push_back(action);
      marks.push_back(mark);
    }
    signature_count = actions.size();
  }
  void check_kernel() {
    // Independent generator: zero/one/two disjoint edge blocks or one triangle,
    // then inject these and the remaining singleton blocks into outputs.
    // This never invokes the direct input-assignment recursion.
    int n = core.n;
    map<Action, Mark> independent;
    vector<vector<int>> literal_maps;
    vector<vector<int>> possible_blocks;
    for (auto [u, v] : edges)
      possible_blocks.push_back({u, v});
    for (int u = 0; u < n; ++u)
      for (int v = u + 1; v < n; ++v)
        for (int w = v + 1; w < n; ++w)
          if (index[u][v] >= 0 && index[u][w] >= 0 && index[v][w] >= 0)
            possible_blocks.push_back({u, v, w});
    vector<vector<int>> matchings(1);
    for (size_t i = 0; i < edges.size(); ++i) {
      matchings.push_back({int(i)});
      for (size_t j = i + 1; j < edges.size(); ++j) {
        auto [u, v] = edges[i];
        auto [x, y] = edges[j];
        if (u != x && u != y && v != x && v != y)
          matchings.push_back({int(i), int(j)});
      }
    }
    for (int block = edges.size(); block < int(possible_blocks.size()); ++block)
      matchings.push_back({block});
    for (int k = 0; k <= min(fixed() - 1 - __builtin_popcount(unsigned(B | C)),
                             STATE_COUNT - fixed());
         ++k) {
      int N = fixed() + k;
      for (const auto &matching : matchings) {
        vector<vector<int>> blocks;
        vector<bool> assigned(N, false);
        int deficiency = 0;
        for (int block : matching) {
          blocks.push_back(possible_blocks[block]);
          deficiency += int(possible_blocks[block].size()) - 1;
          for (int u : possible_blocks[block]) {
            assert(!assigned[u]);
            assigned[u] = true;
          }
        }
        for (int q = 0; q < N; ++q)
          if (!assigned[q])
            blocks.push_back({q});
        assert(deficiency <= 2 && int(blocks.size()) == N - deficiency);
        for (int preA : {1 << n, B})
          for (int preB : {1 << n, B, C})
            for (int preC : fibers) {
              vector<vector<int>> options(blocks.size());
              for (size_t b = 0; b < blocks.size(); ++b)
                for (int output = 0; output < N; ++output) {
                  bool possible = true;
                  for (int input : blocks[b]) {
                    if (input >= fixed() && (output >= fixed() || output == n ||
                                             ((B | C) >> output & 1)))
                      possible = false;
                    if (bool(preA >> input & 1) != (output == n))
                      possible = false;
                    if (bool(preB >> input & 1) != bool(B >> output & 1))
                      possible = false;
                    if (bool(preC >> input & 1) != bool(C >> output & 1))
                      possible = false;
                  }
                  if (possible)
                    options[b].push_back(output);
                }
              vector<int> order(blocks.size());
              iota(order.begin(), order.end(), 0);
              stable_sort(order.begin(), order.end(), [&](int u, int v) {
                return options[u].size() < options[v].size();
              });
              vector<int> f(N, -1);
              function<void(int, unsigned)> inject = [&](int at,
                                                         unsigned used) {
                if (at == int(blocks.size())) {
                  auto edge_destination = [&](int u, int v) {
                    if (u == v)
                      return -1;
                    if (u > v)
                      swap(u, v);
                    auto it = find(edges.begin(), edges.end(), make_pair(u, v));
                    return it == edges.end() ? -2 : int(it - edges.begin());
                  };
                  for (int m = n; m < fixed(); ++m)
                    if (mandatory(m))
                      for (int q = 0; q < N; ++q)
                        if (q != m && edge_destination(f[m], f[q]) >= -1)
                          return;
                  for (auto [u, v] : long_pairs)
                    if (v < N && edge_destination(f[u], f[v]) >= -1)
                      return;
                  if (!fourth_allowed(f))
                    return;
                  if (!safe_rank(f, STATE_COUNT - 3, 3, true) || !safe_rank(f, SAFE_SIZE, SAFE_DEPTH - 3, true))
                    return;
                  for (int level = 4; level <= depth(); ++level)
                    if (!safe_rank(f, SAFE_SIZE, SAFE_DEPTH - level, true, level))
                      return;
                  ++kernel_domains;
                  literal_maps.push_back(canonical_map(f));
                  Action action;
                  for (auto [u, v] : edges)
                    action.pair.push_back(edge_destination(f[u], f[v]));
                  for (int u = 0; u < N; ++u)
                    for (int v = u + 1; v < N; ++v)
                      if (find(edges.begin(), edges.end(), make_pair(u, v)) ==
                          edges.end()) {
                        int t = edge_destination(f[u], f[v]);
                        assert(t != -1);
                        if (t >= 0)
                          action.forced |= 1U << t;
                      }
                  power_edges(f, action);
                  Mark &mark = independent[action];
                  for (int level = 5; level <= depth(); ++level) {
                    int pre = 0;
                    for (int q = 0; q < N; ++q)
                      if (fiber_at(level - 1) >> f[q] & 1)
                        pre |= 1 << q;
                    if (pre == fiber_at(level))
                      mark.flags |= 1U << (level - 1);
                  }
                  if (E) {
                    int pre = 0;
                    for (int q = 0; q < N; ++q)
                      if (D >> f[q] & 1)
                        pre |= 1 << q;
                    if (pre == E)
                      mark.flags |= 8;
                  }
                  mark.arrows[qj()] |= 1U << qj();
                  for (int q = 0; q < N; ++q)
                    mark.arrows[q < fixed() ? q : qj()] |=
                        1U << (f[q] < fixed() ? f[q] : qj());
                  set<int> actualA, actualB, actualC, expectedB, expectedC,
                      expectedD;
                  for (int q = 0; q < N; ++q) {
                    if (f[q] == n)
                      actualA.insert(q);
                    if (B >> f[q] & 1)
                      actualB.insert(q);
                    if (C >> f[q] & 1)
                      actualC.insert(q);
                  }
                  for (int q = 0; q < N; ++q) {
                    if (B >> q & 1)
                      expectedB.insert(q);
                    if (C >> q & 1)
                      expectedC.insert(q);
                    if (D >> q & 1)
                      expectedD.insert(q);
                  }
                  if (actualA == expectedB)
                    mark.flags |= 1;
                  if (actualB == expectedC)
                    mark.flags |= 2;
                  if (actualC == expectedD)
                    mark.flags |= 4;
                  return;
                }
                int b = order[at];
                for (int output : options[b])
                  if (!(used >> output & 1)) {
                    if (!fresh_anonymous_output(output, used))
                      continue;
                    bool sorted = true;
                    for (int input : blocks[b])
                      if (!sorted_anonymous_input(input, output, f))
                        sorted = false;
                    if (!sorted)
                      continue;
                    bool early_valid = true;
                    for (int input : blocks[b])
                      for (int previous = 0; previous < N; ++previous)
                        if (f[previous] >= 0) {
                          bool distant =
                              mandatory(input) || mandatory(previous) ||
                              find(long_pairs.begin(), long_pairs.end(),
                                   make_pair(min(input, previous),
                                             max(input, previous))) !=
                                  long_pairs.end();
                          if (distant && target(output, f[previous]) >= -1)
                            early_valid = false;
                        }
                    if (!early_valid)
                      continue;
                    for (int input : blocks[b])
                      f[input] = output;
                    if (partial_flags(f))
                      inject(at + 1, used | (1U << output));
                    for (int input : blocks[b])
                      f[input] = -1;
                  }
              };
              inject(0, 0);
            }
      }
    }
    sort(raw_maps.begin(), raw_maps.end());
    sort(literal_maps.begin(), literal_maps.end());
    assert(adjacent_find(raw_maps.begin(), raw_maps.end()) == raw_maps.end());
    assert(adjacent_find(literal_maps.begin(), literal_maps.end()) ==
           literal_maps.end());
    assert(raw_maps == literal_maps);
    assert(kernel_domains == domains && independent.size() == actions.size());
    size_t j = 0;
    for (const auto &[action, mark] : independent) {
      assert(!(action < actions[j]) && !(actions[j] < action));
      assert(mark.flags == marks[j].flags && mark.arrows == marks[j].arrows);
      ++j;
    }
  }
  bool valid_p1(const vector<int> &e) const {
    if (core.id >= 100)
      return true; // The two-cover P1 classification does not apply.
    vector<int> degree(core.n, 0);
    int count = 0;
    for (size_t i = 0; i < edges.size(); ++i)
      if (e[i] == 1) {
        ++count;
        ++degree[edges[i].first];
        ++degree[edges[i].second];
      }
    int vertices =
        count_if(degree.begin(), degree.end(), [](int x) { return x > 0; });
    if (count == 1)
      return vertices == 2; // K2
    if (count == 2)
      return vertices == 3 || vertices == 4; // P3 or 2K2
    if (count == 3 && vertices == 3)
      return true; // K3
    if (count == 3 && vertices == 4 &&
        *max_element(degree.begin(), degree.end()) == 2)
      return true; // P4; a triangle plus an isolated edge would have four
                   // edges.
    return false;
  }
  void distances() {
    int ne = edges.size();
    vector<int> e(ne, 1);
    do {
      vector<int> pool;
      unsigned supplies = 0, flags = 0;
      array<unsigned, STATE_COUNT + 1> graph{};
      for (size_t j = 0; j < actions.size(); ++j) {
        const Action &a = actions[j];
        bool allowed = true;
        for (int u = 0; u < ne; ++u) {
          int v = a.pair[u];
          if ((a.not_one >> u & 1) && e[u] == 1)
            allowed = false;
          if (a.forced >> u & 1 && e[u] != 3)
            allowed = false;
          if (v == -1 && e[u] != 1)
            allowed = false;
          if (v >= 0 && e[u] > 1 + e[v])
            allowed = false;
        }
        if (!allowed)
          continue;
        pool.push_back(j);
        flags |= marks[j].flags;
        for (int u = 0; u < ne; ++u) {
          int v = a.pair[u];
          if ((v == -1 && e[u] == 1) || (v >= 0 && e[u] == 1 + e[v]))
            supplies |= 1U << u;
        }
        for (int q = 0; q <= qj(); ++q)
          graph[q] |= marks[j].arrows[q];
      }
      // Independent reverse-pair BFS checks exact distances in the maximal
      // compatible pool; equality is equivalent to all descent suppliers.
      vector<int> actual = pair_bfs(ne, actions, pool);
      bool supplied = supplies == (1U << ne) - 1;
      assert(supplied == (actual == e));
      if (supplied && flags == ((1U << depth()) - 1) &&
          *max_element(e.begin(), e.end()) == 3) {
        if (!valid_p1(e)) {
          ++invalid_p1;
        } else {
          ++joint;
          bool connected = true;
          for (int start = 0; start <= qj(); ++start) {
            unsigned visited = 1U << start;
            queue<int> todo;
            todo.push(start);
            while (!todo.empty()) {
              int u = todo.front();
              todo.pop();
              for (int v = 0; v <= qj(); ++v)
                if ((graph[u] >> v & 1) && !(visited >> v & 1)) {
                  visited |= 1U << v;
                  todo.push(v);
                }
            }
            if (visited != (1U << (qj() + 1)) - 1)
              connected = false;
          }
          // Floyd transitive closure is independent of the per-source queue
          // BFS.
          auto closure = graph;
          for (int q = 0; q <= qj(); ++q)
            closure[q] |= 1U << q;
          for (int k = 0; k <= qj(); ++k)
            for (int q = 0; q <= qj(); ++q)
              if (closure[q] >> k & 1)
                closure[q] |= closure[k];
          bool floyd = true;
          for (int q = 0; q <= qj(); ++q)
            if (closure[q] != (1U << (qj() + 1)) - 1)
              floyd = false;
          assert(connected == floyd);
          if (connected && joint_words(e)) {
            ++sc;
            terminal_probe();
            derive_extensions(e);
            survivor_vectors.push_back(e);
          }
        }
      }
      int u = 0;
      while (u < ne && ++e[u] == 4) {
        e[u] = 1;
        ++u;
      }
      if (u == ne)
        break;
    } while (true);
  }
  Action profile(const vector<int> &f) const {
    Action result;
    for (auto [u, v] : edges)
      result.pair.push_back(target(f[u], f[v]));
    for (int u = 0; u < int(f.size()); ++u)
      for (int v = u + 1; v < int(f.size()); ++v)
        if (index[u][v] < 0) {
          int t = target(f[u], f[v]);
          if (t >= 0)
            result.forced |= 1U << t;
        }
    power_edges(f, result);
    return result;
  }
  static bool compatible(const Action &action, const vector<int> &e) {
    for (size_t u = 0; u < e.size(); ++u) {
      int v = action.pair[u];
      if ((action.not_one >> u & 1) && e[u] == 1)
        return false;
      if ((action.forced >> u & 1) && e[u] != 3)
        return false;
      if (v == -1 && e[u] != 1)
        return false;
      if (v >= 0 && e[u] > 1 + e[v])
        return false;
    }
    return true;
  }
  uint64_t word_nodes = 0, word_pair_checks = 0, word_exclusions = 0,
           word_max_groups = 0;
  vector<vector<int>> word_witness;
  bool joint_words(const vector<int> &e) {
    if (fixed() < STATE_COUNT - 1)
      return true;
    vector<pair<unsigned, int>> seeds;
    for (int level = 4; level <= depth(); ++level) {
      const auto &family = family_cache.at({SAFE_SIZE, level}).first;
      if (int(family.size()) == STATE_COUNT - 1 - level)
        for (unsigned mask : family)
          seeds.push_back({mask, level});
    }
    if (seeds.empty())
      return true;
    vector<vector<int>> alphabet;
    vector<unsigned> supplies;
    for (size_t j = 0; j < raw_maps.size(); ++j)
      if (compatible(raw_profiles[j], e)) {
        auto f = raw_maps[j];
        for (int q = f.size(); q < STATE_COUNT; ++q)
          f.push_back(q);
        unsigned flags = 0;
        for (int i = 0; i < depth(); ++i) {
          unsigned pre = 0;
          for (int q = 0; q < STATE_COUNT; ++q)
            if (fiber_at(i) >> f[q] & 1)
              pre |= 1U << q;
          if (pre == unsigned(fiber_at(i + 1)))
            flags |= 1U << i;
        }
        const auto &action = raw_profiles[j];
        for (size_t i = 0; i < edges.size(); ++i) {
          int v = action.pair[i];
          if ((v == -1 && e[i] == 1) || (v >= 0 && e[i] == e[v] + 1))
            flags |= 1U << (depth() + i);
        }
        alphabet.push_back(move(f));
        supplies.push_back(flags);
      }
    auto answer = short_word_clique<STATE_COUNT>(alphabet, supplies,
                                    (1U << (depth() + edges.size())) - 1,
                                    core.n, seeds, edges, e);
    word_max_groups = max(word_max_groups, uint64_t(answer.groups));
    word_nodes += answer.nodes;
    word_pair_checks += answer.pair_checks;
    if (!answer.possible)
      ++word_exclusions;
    word_witness.clear();
    for (int i : answer.witness)
      word_witness.push_back(alphabet[i]);
    return answer.possible;
  }
  void terminal_probe() const {
    if (depth() != SAFE_DEPTH)
      return;
    if (fixed() < STATE_COUNT - 1) {
      cout << "TERMINAL_UNRESOLVED fixed=" << fixed() << endl;
      return;
    }
    auto alphabet = word_witness;
    assert(!alphabet.empty());
    const auto &initial = family_cache.at({SAFE_SIZE, SAFE_DEPTH}).first;
    assert(initial.size() == 1);
    unsigned S = initial[0];
    auto image = [&](unsigned mask, const vector<int> &f) {
      unsigned out = 0;
      for (int q = 0; q < STATE_COUNT; ++q)
        if (mask >> q & 1)
          out |= 1U << f[q];
      return out;
    };
    auto search = [&](unsigned start, int mode) {
      vector<int> distance(MASK_COUNT, -1);
      queue<unsigned> todo;
      todo.push(start);
      distance[start] = 0;
      while (!todo.empty()) {
        unsigned mask = todo.front();
        todo.pop();
        bool goal =
            mode == 0 ? (__builtin_popcount(mask) < SAFE_SIZE || !(mask >> core.n & 1))
                      : (mode == 1 ? mask == S : __builtin_popcount(mask) == 1);
        if (goal)
          return distance[mask];
        for (const auto &f : alphabet) {
          unsigned out = image(mask, f);
          if (distance[out] < 0) {
            distance[out] = distance[mask] + 1;
            todo.push(out);
          }
        }
      }
      return -1;
    };
    cout << "TERMINAL T=" << core.id << " S=" << S
         << " letters=" << alphabet.size() << " ac=" << search(S, 0)
         << " reach=" << search(MASK_COUNT - 1, 1) << " reset=" << search(MASK_COUNT - 1, 2)
         << endl;
    for (const auto &f : alphabet) {
      cout << "CANDIDATE_LETTER";
      for (int q : f)
        cout << " " << q;
      cout << endl;
    }
  }
  void derive_extensions(const vector<int> &e) {
    if (depth() >= limit)
      return;
    vector<int> old = E ? closure(depth()) : all_third;
    int source = fiber_at(depth());
    for (size_t map_index = 0; map_index < raw_maps.size(); ++map_index)
      if (compatible(raw_profiles[map_index], e)) {
        const auto &f = raw_maps[map_index];
        unsigned pre = 0;
        for (int q = 0; q < int(f.size()); ++q)
          if (source >> f[q] & 1)
            pre |= 1U << q;
        if (find(old.begin(), old.end(), int(pre)) != old.end())
          continue;
        // A new actual preimage is a short one-count clique. Arrival and
        // antichain restrictions apply only when its word length is <=7.
        if (!pre || (depth() < 7 && __builtin_popcount(pre) == 1 &&
                     __builtin_ctz(pre) < core.n))
          continue;
        bool allowed = true;
        if (depth() < 7)
          for (int mask : old)
            if (pre != unsigned(mask) &&
                ((pre & mask) == pre || (pre & mask) == unsigned(mask)))
              allowed = false;
        if (depth() < 7)
          for (auto [u, v] : long_pairs)
            if ((pre >> u & 1) && (pre >> v & 1))
              allowed = false;
        if (!allowed)
          continue;
        int outside = 0, normalized = pre & ((1 << fixed()) - 1);
        for (int q = fixed(); q < int(f.size()); ++q)
          if (pre >> q & 1) {
            normalized |= 1 << (fixed() + outside);
            ++outside;
          }
        assert(outside <= STATE_COUNT - fixed());
        extensions.insert(normalized);
      }
    // H_(k+1) strictly extends H_k, so at least one of these actual preimages
    // must occur in any real alphabet. All next-stage jobs come from this set.
  }
  string run() {
    generate();
    check_kernel();
    for (const auto &f : raw_maps)
      raw_profiles.push_back(profile(f));
    distances();
    ostringstream out;
    unsigned allflags = 0;
    for (auto m : marks)
      allflags |= m.flags;
    out << "T=" << core.id << " Bmask=" << B << " Cmask=" << C << " Dmask=" << D
        << " Emask=" << E << " Fmask=" << F << " Gmask=" << G << " Hmask=" << H
        << " Imask=" << I << " Jmask=" << J << " Kmask=" << K << " Lmask=" << L
        << " allflags=" << allflags << " domain=" << domains
        << " kernel_domain=" << kernel_domains
        << " signatures=" << signature_count << " invalid_P1=" << invalid_p1
        << " joint=" << joint << " word_excluded=" << word_exclusions
        << " word_nodes=" << word_nodes << " word_pairs=" << word_pair_checks
        << " word_groups=" << word_max_groups << " SC=" << sc << '\n';
    for (const auto &e : survivor_vectors) {
      out << "SC_vector";
      for (int x : e)
        out << ' ' << x;
      out << '\n';
    }
    if (!extensions.empty()) {
      out << "EXTENSIONS level=" << depth() + 1;
      for (int mask : extensions)
        out << ' ' << mask;
      out << '\n';
    }
    return out.str();
  }
};
void controls() {
  short_word_clique_controls<STATE_COUNT>();
  for (int divisor = 2; divisor * divisor <= 65521; ++divisor)
    assert(65521 % divisor);
  // A synthetic three-edge chain is accepted, while a missing final supplier
  // leaves every edge at infinite distance. These are algorithm controls only.
  vector<Action> a = {{{-1, 0, 1}, 0}};
  assert((pair_bfs(3, a, {0}) == vector<int>{1, 2, 3}));
  assert((pair_bfs(3, a, {}) == vector<int>{99, 99, 99}));
  assert(Case::compatible(a[0], {1, 2, 3}));
  assert(!Case::compatible(a[0], {2, 2, 3}));
  a[0].forced = 1;
  assert(!Case::compatible(a[0], {1, 2, 3}));
  Case trial(cores[3], 3, 18, 9);
  assert(trial.prepare());
  vector<int> identity(STATE_COUNT);
  iota(identity.begin(), identity.end(), 0);
  vector<int> collapse(STATE_COUNT, 0);
  for (bool exact : {false, true}) {
    assert(trial.safe_rank(identity, SAFE_SIZE, SAFE_DEPTH - 3, exact));
    assert(trial.safe_rank(identity, STATE_COUNT - 3, 3, exact));
    assert(!trial.safe_rank(collapse, SAFE_SIZE, SAFE_DEPTH - 3, exact));
    assert(!trial.safe_rank(collapse, STATE_COUNT - 3, 3, exact));
  }
  // Exhaust every graph on six vertices: branch-on-an-uncovered-edge is
  // checked against literal three-subset covers. Also cover an eight-point
  // four-edge matching, beyond the six-vertex control domain.
  vector<pair<int, int>> pairs;
  for (int u = 0; u < 6; ++u)
    for (int v = u + 1; v < 6; ++v)
      pairs.push_back({u, v});
  for (unsigned mask = 0; mask < (1U << pairs.size()); ++mask) {
    vector<int> cliques;
    for (size_t i = 0; i < pairs.size(); ++i)
      if (mask >> i & 1)
        cliques.push_back((1 << pairs[i].first) | (1 << pairs[i].second));
    bool literal = false;
    for (unsigned cover = 0; cover < 64; ++cover)
      if (__builtin_popcount(cover) == 3) {
        bool valid = true;
        for (int edge : cliques)
          if (!(cover & unsigned(edge)))
            valid = false;
        literal |= valid;
      }
    assert(trial.cover_three(cliques) == literal);
  }
  assert(!trial.cover_three({3, 12, 48, 192}));
  // Exact equality of retained literal-map sets also checks rejection decisions
  // between the two generators and rank methods; no stored records are read.
  cout << "CONTROLS distance, rank, nonedge constraints, and all 32768 "
          "six-point cover graphs and 512 short-word pools "
          "PASS"
       << endl;
}
int main(int argc, char **argv) {
  controls();
  int threads = 4, max_depth = 11, only_core = -1;
  bool disjoint = false, tau3 = false, quotient = false, all_entrances = false;
  int first_size = 2, second_size = 2;
  vector<int> explicit_flag;
  for (int i = 1; i < argc; ++i) {
    if (string(argv[i]) == "--flag" && i + 11 < argc) {
      for (int k = 0; k < 11; ++k)
        explicit_flag.push_back(stoi(argv[++i]));
      first_size = __builtin_popcount(unsigned(explicit_flag[0]));
      second_size = __builtin_popcount(unsigned(explicit_flag[1]));
      disjoint = true;
    } else if (string(argv[i]) == "--all-entrances") {
      all_entrances = true;
      disjoint = true;
    } else if (string(argv[i]) == "--core" && i + 1 < argc)
      only_core = stoi(argv[++i]);
    else if (string(argv[i]) == "--quotient")
      quotient = true;
    else if (string(argv[i]) == "--sizes" && i + 2 < argc) {
      first_size = stoi(argv[++i]);
      second_size = stoi(argv[++i]);
      disjoint = true;
    } else if (string(argv[i]) == "--tau3-disjoint" ||
               string(argv[i]) == "--tau3") {
      disjoint = true;
      tau3 = true;
    } else if (string(argv[i]) == "--disjoint")
      disjoint = true;
    else if (string(argv[i]) == "--depth" && i + 1 < argc)
      max_depth = stoi(argv[++i]);
    else if (string(argv[i]) == "--threads" && i + 1 < argc)
      threads = stoi(argv[++i]);
    else
      return 2;
  }
  if (threads < 1 || threads > 32 || max_depth < 3 || max_depth > 11 ||
      first_size < 1 || first_size > 2 || second_size < 1 || second_size > 2)
    return 2;
  if (!explicit_flag.empty() &&
      (only_core < 0 || any_of(
                            explicit_flag.begin(), explicit_flag.end(),
                            [](int m) { return m < 0 || m >= MASK_COUNT; })))
    return 2;
  struct Job {
    Core core;
    int B, C, D, E, F, G, H, I, J, K, L;
  };
  vector<Job> jobs;
  int initial_choices = 0, canonical_choices = 0;
  map<int, vector<vector<int>>> symmetry_groups;
  auto domain_cores = cores;
  if (disjoint)
    domain_cores.push_back({5, 5, "01 02 03 12 14"});
  if (all_entrances || first_size == 1 || second_size == 1) {
    domain_cores.push_back({0, 3, "01 02 12"});
    domain_cores.push_back({1, 4, "01 02 03 12"});
    domain_cores.push_back({2, 4, "01 02 03 12 13"});
  }
  if (tau3)
    domain_cores = {
        {101, 5, "01 23 24 34"},       {102, 5, "03 12 14 24 34"},
        {103, 5, "03 04 12 14 23"},    {104, 5, "04 12 13 23 24 34"},
        {105, 5, "03 04 12 14 23 34"}, {106, 6, "05 14 23"},
        {107, 6, "05 14 23 45"},       {108, 6, "05 14 23 35 45"},
        {109, 6, "05 14 23 25 34"},    {110, 6, "05 14 23 34 35 45"},
        {111, 6, "05 14 23 25 34 45"}};
  if (tau3 && all_entrances)
    domain_cores.push_back({100, 4, "01 02 03 12 13 23"});
  if (only_core >= 0 &&
      none_of(domain_cores.begin(), domain_cores.end(),
              [&](const Core &c) { return c.id == only_core; }))
    return 2;
  for (auto core : domain_cores) {
    if (only_core >= 0 && only_core != core.id)
      continue;
    if (!explicit_flag.empty()) {
      const auto &a = explicit_flag;
      jobs.push_back({core, a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7],
                      a[8], a[9], a[10]});
      ++initial_choices;
      ++canonical_choices;
      continue;
    }
    vector<int> edges;
    istringstream input(core.text);
    string edge;
    while (input >> edge)
      edges.push_back((1 << (edge[0] - '0')) | (1 << (edge[1] - '0')));
    vector<vector<int>> automorphisms;
    vector<int> permutation(core.n);
    iota(permutation.begin(), permutation.end(), 0);
    auto transform = [&](int mask, const vector<int> &perm) {
      int result = mask & ~((1 << core.n) - 1);
      for (int q = 0; q < core.n; ++q)
        if (mask >> q & 1)
          result |= 1 << perm[q];
      return result;
    };
    do {
      bool valid = true;
      for (int edge : edges)
        if (find(edges.begin(), edges.end(), transform(edge, permutation)) ==
            edges.end())
          valid = false;
      if (valid)
        automorphisms.push_back(permutation);
    } while (next_permutation(permutation.begin(), permutation.end()));
    symmetry_groups[core.id] = automorphisms;
    vector<int> core_cliques;
    for (int mask = 1; mask < (1 << core.n); ++mask) {
      if (__builtin_popcount(unsigned(mask)) < 2)
        continue;
      bool clique = true;
      for (int u = 0; u < core.n; ++u)
        for (int v = u + 1; v < core.n; ++v)
          if ((mask >> u & 1) && (mask >> v & 1) &&
              find(edges.begin(), edges.end(), (1 << u) | (1 << v)) ==
                  edges.end())
            clique = false;
      if (clique)
        core_cliques.push_back(mask);
    }
    vector<int> first =
        first_size == 2 ? edges : vector<int>{1 << (core.n + 1)};
    if (all_entrances) {
      first = {1 << (core.n + 1)};
      for (int mask : core_cliques)
        if (__builtin_popcount(unsigned(mask)) <= 3)
          first.push_back(mask);
    }
    for (int B : first) {
      bool singleton_B = __builtin_popcount(unsigned(B)) == 1;
      vector<int> second = second_size == 2
                               ? edges
                               : vector<int>{1 << (core.n + 1 + singleton_B)};
      if (all_entrances) {
        second = {1 << (core.n + 1 + singleton_B)};
        for (int mask : core_cliques)
          if (__builtin_popcount(unsigned(mask)) <= 3)
            second.push_back(mask);
      }
      for (int C : second) {
        if (B == C || (all_entrances ? ((B & C) == B || (B & C) == C)
                                     : __builtin_popcount(unsigned(B & C)) !=
                                           (disjoint ? 0 : 1)))
          continue;
        auto third = core_cliques;
        third.push_back(1 << (core.n + 1 + singleton_B +
                              (__builtin_popcount(unsigned(C)) == 1)));
        for (int D : third)
          if (D != B && D != C) {
            ++initial_choices;
            bool canonical = true;
            if (quotient)
              for (const auto &perm : automorphisms)
                if (vector<int>{transform(B, perm), transform(C, perm),
                                transform(D, perm)} < vector<int>{B, C, D})
                  canonical = false;
            if (!canonical)
              continue;
            ++canonical_choices;
            Case trial(core, B, C, D);
            if (trial.prepare())
              jobs.push_back({core, B, C, D, 0, 0, 0, 0, 0, 0, 0, 0});
          }
      }
    }
  }
  cout << "PARAMETERS n=" << STATE_COUNT << " s=" << SAFE_SIZE
       << " target=" << STATE_COUNT - 1 << " represented_depth=11" << endl;
  cout << "INITIAL choices=" << initial_choices
       << " symmetry_kept=" << canonical_choices
       << " family_reject=" << canonical_choices - int(jobs.size())
       << " admitted=" << jobs.size() << " all_entrances=" << all_entrances
       << endl;
  auto key = [](const Job &job) {
    return array<int, 12>{job.core.id, job.B, job.C, job.D, job.E, job.F,
                          job.G,       job.H, job.I, job.J, job.K, job.L};
  };
  auto canonical_job = [&](Job job) {
    if (!quotient)
      return job;
    auto best = key(job);
    for (const auto &perm : symmetry_groups[job.core.id]) {
      auto candidate = key(job);
      for (int i = 1; i < 12; ++i) {
        int mask = candidate[i], out = mask & ~((1 << job.core.n) - 1);
        for (int q = 0; q < job.core.n; ++q)
          if (mask >> q & 1)
            out |= 1 << perm[q];
        candidate[i] = out;
      }
      if (candidate < best)
        best = candidate;
    }
    return Job{job.core, best[1], best[2], best[3], best[4],  best[5],
               best[6],  best[7], best[8], best[9], best[10], best[11]};
  };
  auto stage = [&](const vector<Job> &domain, vector<Job> &next_jobs) {
    atomic<int> next{0}, complete{0};
    atomic<uint64_t> total_sc{0};
    mutex output;
    vector<thread> workers;
    for (int t = 0; t < threads; ++t)
      workers.emplace_back([&] {
        for (int j; (j = next.fetch_add(1)) < int(domain.size());) {
          auto job = domain[j];
          Case trial(job.core, job.B, job.C, job.D, job.E, job.F, job.G, job.H,
                     job.I, job.J, job.K, job.L);
          trial.limit = max_depth;
          if (!trial.prepare()) {
            ++complete;
            lock_guard<mutex> guard(output);
            cout << "FAMILY_REJECT T=" << job.core.id << " B=" << job.B
                 << " C=" << job.C << " D=" << job.D << " E=" << job.E
                 << " F=" << job.F << " G=" << job.G << " H=" << job.H
                 << " I=" << job.I << " J=" << job.J << " K=" << job.K
                 << " L=" << job.L << endl;
            continue;
          }
          string result = trial.run();
          total_sc.fetch_add(trial.sc);
          ++complete;
          lock_guard<mutex> guard(output);
          cout << result << flush;
          for (int extension : trial.extensions) {
            Job next_job = job;
            if (!job.E)
              next_job.E = extension;
            else if (!job.F)
              next_job.F = extension;
            else if (!job.G)
              next_job.G = extension;
            else if (!job.H)
              next_job.H = extension;
            else if (!job.I)
              next_job.I = extension;
            else if (!job.J)
              next_job.J = extension;
            else if (!job.K)
              next_job.K = extension;
            else if (!job.L)
              next_job.L = extension;
            else
              assert(false);
            next_jobs.push_back(canonical_job(next_job));
          }
        }
      });
    for (auto &worker : workers)
      worker.join();
    assert(complete == int(domain.size()));
    sort(next_jobs.begin(), next_jobs.end(),
         [&](const Job &a, const Job &b) { return key(a) < key(b); });
    next_jobs.erase(
        unique(next_jobs.begin(), next_jobs.end(),
               [&](const Job &a, const Job &b) { return key(a) == key(b); }),
        next_jobs.end());
    cout << "COMPLETE cases=" << complete << " requested=" << domain.size()
         << " SC_total=" << total_sc << endl;
    return total_sc.load();
  };
  vector<Job> fourth, unused;
  uint64_t third_survivors = stage(jobs, fourth);
  if (disjoint) {
    uint64_t survivors = third_survivors;
    for (int level = 4; level <= max_depth && !fourth.empty(); ++level) {
      cout << "FLAG level=" << level << " generated=" << fourth.size() << endl;
      unused.clear();
      survivors = stage(fourth, unused);
      fourth = move(unused);
    }
    cout << "SCOPE " << (all_entrances ? "all entrances " : "disjoint ")
         << (tau3 ? "tau3" : "tau2") << " with flag limit " << max_depth
         << "; all_entrances=" << all_entrances << "; entry sizes "
         << (all_entrances
                 ? "1..3 (all ordered combinations)"
                 : to_string(first_size) + "," + to_string(second_size))
         << "; quotient=" << quotient << "; core=" << only_core << endl;
    return survivors ? 3 : 0;
  }
  if (max_depth == 3)
    return third_survivors ? 3 : 0;
  uint64_t survivors = stage(fourth, unused);
  assert(unused.empty());
  return survivors ? 3 : 0;
}
