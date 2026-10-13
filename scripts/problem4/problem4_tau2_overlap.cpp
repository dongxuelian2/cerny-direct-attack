// Complete third/fourth-fiber relaxation for the nine triangle-free cores.
// Mathematical scope and completeness: PROOF.md#problem4-overlap-nine-cores.
// Exit 3 means relaxation survivors remain; it never certifies a DFA.
// Representatives model ONE letter; never iterate anonymous isolated labels.
// Direct input assignments are independently checked by matching-kernel
// blocks with injective outputs, including profile, flags, and arrow unions.
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
struct Core {
  int id, n;
  string text;
};
const vector<Core> cores = {
    {3, 4, "01 02 13"},       {4, 4, "01 02 13 23"},       {6, 5, "01 02 03 14"},
    {7, 5, "01 02 03 14 24"}, {8, 5, "01 02 03 14 24 34"}, {9, 5, "01 02 13 24"},
    {10, 5, "01 02 34"},      {11, 6, "01 02 03 14 15"},   {12, 6, "01 02 34 35"}};
struct Action {
  vector<int> pair;
  unsigned forced = 0;
  bool operator<(const Action &b) const {
    return pair != b.pair ? pair < b.pair : forced < b.forced;
  }
};
// Distances only on the explicit P3 edges. An image outside P3 cannot
// supply a length <=3, so it has no arc in this reverse BFS.
vector<int> pair_bfs(int count, const vector<Action> &actions, const vector<int> &pool) {
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
  array<unsigned, 14> arrows{};
  unsigned flags = 0;
};
struct Case {
  Core core;
  int B, C, D, E;
  int fixed() const {
    return core.n + 1 + (__builtin_popcount(unsigned(D)) == 1 || (E >> (core.n + 1)));
  }
  int qj() const { return fixed(); }
  set<int> extensions;
  vector<vector<int>> raw_maps;
  vector<pair<int, int>> edges, long_pairs;
  vector<int> fibers, fourth_fibers;
  int index[14][14];
  vector<Action> actions;
  vector<Mark> marks;
  uint64_t domains = 0, signature_count = 0, joint = 0, sc = 0, kernel_domains = 0;
  vector<vector<int>> survivor_vectors;
  uint64_t invalid_p1 = 0;

  Case(Core h, int b, int c, int d, int e = 0) : core(h), B(b), C(c), D(d), E(e) {
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
  bool prepare() {
    int n = core.n;
    vector<vector<int>> fib(n);
    vector<int> color(n, -1), component(n, -1);
    for (int mask : {B, C, D}) {
      if (__builtin_popcount(unsigned(mask)) == 1)
        continue;
      int u = __builtin_ctz(unsigned(mask));
      int v = __builtin_ctz(unsigned(mask & ~(1 << u)));
      fib[u].push_back(v);
      fib[v].push_back(u);
    }
    int part = 0;
    for (int start = 0; start < n; ++start)
      if (!fib[start].empty() && color[start] < 0) {
        color[start] = 0;
        component[start] = part;
        queue<int> todo;
        todo.push(start);
        while (!todo.empty()) {
          int u = todo.front();
          todo.pop();
          for (int v : fib[u]) {
            if (color[v] < 0) {
              color[v] = 1 - color[u];
              component[v] = part;
              todo.push(v);
            } else if (color[v] == color[u])
              return false;
          }
        }
        ++part;
      }
    fibers.push_back(1 << n);
    if (__builtin_popcount(unsigned(D)) == 1)
      fibers.push_back(D);
    for (int u = 0; u < n; ++u)
      for (int v = u + 1; v < n; ++v)
        if (component[u] >= 0 && component[u] == component[v]) {
          if (color[u] == color[v])
            long_pairs.push_back({u, v});
          else if (index[u][v] >= 0)
            fibers.push_back((1 << u) | (1 << v));
        }
    // SF4: if xy is a short one-count fiber and xz is already a P3 edge,
    // yz cannot be a P7 edge. Add all such mandatory long pairs.
    for (int mask : fibers)
      if (__builtin_popcount(unsigned(mask)) == 2) {
        int u = __builtin_ctz(unsigned(mask)), v = __builtin_ctz(unsigned(mask & ~(1 << u)));
        for (int z = 0; z < n; ++z)
          if (z != u && z != v) {
            if (index[u][z] >= 0)
              long_pairs.push_back(minmax(v, z));
            if (index[v][z] >= 0)
              long_pairs.push_back(minmax(u, z));
          }
      }
    sort(long_pairs.begin(), long_pairs.end());
    long_pairs.erase(unique(long_pairs.begin(), long_pairs.end()), long_pairs.end());
    for (auto [u, v] : long_pairs)
      if (index[u][v] >= 0)
        return false;
    assert(find(fibers.begin(), fibers.end(), B) != fibers.end());
    assert(find(fibers.begin(), fibers.end(), C) != fibers.end());
    assert(find(fibers.begin(), fibers.end(), D) != fibers.end());
    if (E) {
      int explicit_n = fixed();
      vector<vector<int>> adj(explicit_n);
      vector<int> col(explicit_n, -1), comp(explicit_n, -1);
      int cc = 0;
      fourth_fibers.push_back(1 << n);
      for (int mask : {B, C, D, E}) {
        if (__builtin_popcount(unsigned(mask)) == 1) {
          if (mask != (1 << n))
            fourth_fibers.push_back(mask);
          continue;
        }
        int u = __builtin_ctz(unsigned(mask)), v = __builtin_ctz(unsigned(mask & ~(1 << u)));
        adj[u].push_back(v);
        adj[v].push_back(u);
      }
      for (int start = 0; start < explicit_n; ++start)
        if (!adj[start].empty() && col[start] < 0) {
          queue<int> todo;
          todo.push(start);
          col[start] = 0;
          comp[start] = cc++;
          while (!todo.empty()) {
            int u = todo.front();
            todo.pop();
            for (int v : adj[u]) {
              if (col[v] < 0) {
                col[v] = 1 - col[u];
                comp[v] = comp[u];
                todo.push(v);
              } else if (col[v] == col[u])
                return false;
            }
          }
        }
      for (int u = 0; u < explicit_n; ++u)
        for (int v = u + 1; v < explicit_n; ++v)
          if (comp[u] >= 0 && comp[u] == comp[v]) {
            if (col[u] == col[v])
              long_pairs.push_back({u, v});
            else
              fourth_fibers.push_back((1 << u) | (1 << v));
          }
      for (int mask : fourth_fibers)
        if (__builtin_popcount(unsigned(mask)) == 2) {
          int u = __builtin_ctz(unsigned(mask)), v = __builtin_ctz(unsigned(mask & ~(1 << u)));
          for (int z = 0; z < n; ++z)
            if (z != u && z != v) {
              if (index[u][z] >= 0)
                long_pairs.push_back(minmax(v, z));
              if (index[v][z] >= 0)
                long_pairs.push_back(minmax(u, z));
            }
        }
      sort(long_pairs.begin(), long_pairs.end());
      long_pairs.erase(unique(long_pairs.begin(), long_pairs.end()), long_pairs.end());
      for (auto [u, v] : long_pairs)
        if (index[u][v] >= 0)
          return false;
    }
    return true;
  }
  int target(int u, int v) const { return u == v ? -1 : index[u][v]; }
  bool mandatory(int u) const {
    return u == core.n || (u == core.n + 1 && ((__builtin_popcount(unsigned(D)) == 1) ||
                                               (E && __builtin_popcount(unsigned(E)) == 1)));
  }
  bool safe_rank(const vector<int> &f, int size, int need, bool exact = false) const {
    // Independent relabelings of anonymous inputs/outputs preserve these full
    // subset families, so the omitted bijection can be the identity here.
    vector<array<long long, 13>> integer_rows;
    constexpr int P = 65521;
    array<array<int, 13>, 13> basis{};
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
      if (size == 9) {
        if (!(mask >> core.n & 1))
          return false;
        for (int fiber : {B, C, D})
          if (__builtin_popcount(mask & unsigned(fiber)) != 1)
            return false;
      }
      return true;
    };
    for (unsigned mask = 0; mask < (1U << 13); ++mask)
      if (__builtin_popcount(mask) == size && family(mask)) {
        unsigned out = 0;
        for (int q = 0; q < 13; ++q)
          if (mask >> q & 1)
            out |= 1U << (q < int(f.size()) ? f[q] : q);
        if (__builtin_popcount(out) != size || !family(out))
          continue;
        if (exact) {
          array<long long, 13> row{};
          for (int q = 0; q < 13; ++q)
            row[q] = mask >> q & 1;
          integer_rows.push_back(row);
          continue;
        }
        array<int, 13> row{};
        for (int q = 0; q < 13; ++q)
          row[q] = mask >> q & 1;
        for (int q = 0; q < 13; ++q)
          if (row[q]) {
            if (!basis[q][q]) {
              int inv = power(row[q], P - 2);
              for (int j = q; j < 13; ++j)
                basis[q][j] = int(1LL * row[j] * inv % P);
              if (++rank >= need)
                return true;
              break;
            }
            int t = row[q];
            for (int j = q; j < 13; ++j)
              row[j] = int((row[j] - 1LL * t * basis[q][j] % P + P) % P);
          }
      }
    if (exact) {
      // Fraction-free, primitive integer row reduction. No modular inverses.
      int at = 0;
      for (int col = 0; col < 13; ++col) {
        int pivot = at;
        while (pivot < int(integer_rows.size()) && !integer_rows[pivot][col])
          ++pivot;
        if (pivot == int(integer_rows.size()))
          continue;
        swap(integer_rows[at], integer_rows[pivot]);
        for (int i = at + 1; i < int(integer_rows.size()); ++i)
          if (integer_rows[i][col]) {
            long long a = integer_rows[at][col], b = integer_rows[i][col], g = 0;
            for (int j = col; j < 13; ++j) {
              integer_rows[i][j] = a * integer_rows[i][j] - b * integer_rows[at][j];
              g = gcd(g, abs(integer_rows[i][j]));
            }
            if (g)
              for (int j = col; j < 13; ++j)
                integer_rows[i][j] /= g;
          }
        if (++at >= need)
          return true;
      }
    }
    return false;
  }
  bool fourth_allowed(const vector<int> &f) const {
    if (!E)
      return true;
    int pre = 0;
    for (int q = 0; q < int(f.size()); ++q)
      if (D >> f[q] & 1)
        pre |= 1 << q;
    if (find(fourth_fibers.begin(), fourth_fibers.end(), pre) == fourth_fibers.end())
      return false;
    for (int fiber : fourth_fibers) {
      unsigned before = 0;
      for (int q = 0; q < int(f.size()); ++q)
        if (fiber >> f[q] & 1)
          before |= 1U << q;
      if (!before)
        return false;
      if (__builtin_popcount(before) == 1 && __builtin_ctz(before) < core.n)
        return false;
      for (int old : fourth_fibers)
        if (before != unsigned(old) &&
            ((before & old) == before || (before & old) == unsigned(old)))
          return false;
      if (fiber == (1 << core.n) || fiber == B || fiber == C || fiber == D || fiber == E)
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
  void generate() {
    int n = core.n;
    map<Action, Mark> signatures;
    for (int k = 0; k <= fixed() - 4; ++k) {
      int N = fixed() + k;
      vector<int> f(N, -1);
      for (int preA : {1 << n, B})
        for (int preB : {1 << n, B, C})
          for (int preC : fibers) {
            vector<vector<int>> allowed(N);
            for (int q = 0; q < N; ++q)
              for (int out = 0; out < N; ++out) {
                if (q >= fixed() && (out >= fixed() || out == n || ((B | C) >> out & 1)))
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
            stable_sort(order.begin(), order.end(),
                        [&](int u, int v) { return allowed[u].size() < allowed[v].size(); });
            function<void(int, unsigned, int)> assign = [&](int at, unsigned outputs,
                                                            int deficiency) {
              if (at == N) {
                assert(__builtin_popcount(outputs) >= N - 2);
                if (!fourth_allowed(f))
                  return;
                if (!E && (!safe_rank(f, 10, 3) || !safe_rank(f, 9, 8)))
                  return;
                ++domains;
                raw_maps.push_back(f);
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
                Mark &mark = signatures[action];
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
                if (preC != (1 << n) && preC != B && preC != C)
                  mark.flags |= 4;
                return;
              }
              int q = order[at];
              for (int out : allowed[q]) {
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
                           make_pair(min(q, other), max(q, other))) != long_pairs.end();
                  if (long_pair && target(out, f[other]) >= -1)
                    ok = false;
                }
                if (!ok)
                  continue;
                f[q] = out;
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
    // Independent generator: enumerate zero, one, or two disjoint core-edge
    // kernel blocks, then inject those blocks and all singleton blocks into
    // outputs. This never invokes the direct input-assignment recursion.
    int n = core.n;
    map<Action, Mark> independent;
    vector<vector<int>> literal_maps;
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
    for (int k = 0; k <= fixed() - 4; ++k) {
      int N = fixed() + k;
      for (const auto &matching : matchings) {
        vector<vector<int>> blocks;
        vector<bool> assigned(N, false);
        for (int edge : matching) {
          auto [u, v] = edges[edge];
          assert(!assigned[u] && !assigned[v]);
          blocks.push_back({u, v});
          assigned[u] = assigned[v] = true;
        }
        for (int q = 0; q < N; ++q)
          if (!assigned[q])
            blocks.push_back({q});
        assert(int(blocks.size()) == N - int(matching.size()));
        for (int preA : {1 << n, B})
          for (int preB : {1 << n, B, C})
            for (int preC : fibers) {
              vector<vector<int>> options(blocks.size());
              for (size_t b = 0; b < blocks.size(); ++b)
                for (int output = 0; output < N; ++output) {
                  bool possible = true;
                  for (int input : blocks[b]) {
                    if (input >= fixed() &&
                        (output >= fixed() || output == n || ((B | C) >> output & 1)))
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
              stable_sort(order.begin(), order.end(),
                          [&](int u, int v) { return options[u].size() < options[v].size(); });
              vector<int> f(N, -1);
              function<void(int, unsigned)> inject = [&](int at, unsigned used) {
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
                    if (edge_destination(f[u], f[v]) >= -1)
                      return;
                  if (!fourth_allowed(f))
                    return;
                  if (!E && (!safe_rank(f, 10, 3, true) || !safe_rank(f, 9, 8, true)))
                    return;
                  ++kernel_domains;
                  literal_maps.push_back(f);
                  Action action;
                  for (auto [u, v] : edges)
                    action.pair.push_back(edge_destination(f[u], f[v]));
                  for (int u = 0; u < N; ++u)
                    for (int v = u + 1; v < N; ++v)
                      if (find(edges.begin(), edges.end(), make_pair(u, v)) == edges.end()) {
                        int t = edge_destination(f[u], f[v]);
                        assert(t != -1);
                        if (t >= 0)
                          action.forced |= 1U << t;
                      }
                  Mark &mark = independent[action];
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
                    mark.arrows[q < fixed() ? q : qj()] |= 1U << (f[q] < fixed() ? f[q] : qj());
                  set<int> actualA, actualB, actualC, expectedB, expectedC;
                  for (int q = 0; q < N; ++q) {
                    if (f[q] == n)
                      actualA.insert(q);
                    if (B >> f[q] & 1)
                      actualB.insert(q);
                    if (C >> f[q] & 1)
                      actualC.insert(q);
                  }
                  for (int q = 0; q < n; ++q) {
                    if (B >> q & 1)
                      expectedB.insert(q);
                    if (C >> q & 1)
                      expectedC.insert(q);
                  }
                  if (actualA == expectedB)
                    mark.flags |= 1;
                  if (actualB == expectedC)
                    mark.flags |= 2;
                  if (actualC != set<int>{n} && actualC != expectedB && actualC != expectedC)
                    mark.flags |= 4;
                  return;
                }
                int b = order[at];
                for (int output : options[b])
                  if (!(used >> output & 1)) {
                    for (int input : blocks[b])
                      f[input] = output;
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
    vector<int> degree(core.n, 0);
    int count = 0;
    for (size_t i = 0; i < edges.size(); ++i)
      if (e[i] == 1) {
        ++count;
        ++degree[edges[i].first];
        ++degree[edges[i].second];
      }
    int vertices = count_if(degree.begin(), degree.end(), [](int x) { return x > 0; });
    if (count == 1)
      return vertices == 2; // K2
    if (count == 2)
      return vertices == 3 || vertices == 4; // P3 or 2K2
    if (count == 3 && vertices == 4 && *max_element(degree.begin(), degree.end()) == 2)
      return true; // P4; a triangle plus an isolated edge would have four edges.
    return false;
  }
  void distances() {
    int ne = edges.size();
    vector<int> e(ne, 1);
    do {
      vector<int> pool;
      unsigned supplies = 0, flags = 0;
      array<unsigned, 14> graph{};
      for (size_t j = 0; j < actions.size(); ++j) {
        const Action &a = actions[j];
        bool allowed = true;
        for (int u = 0; u < ne; ++u) {
          int v = a.pair[u];
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
      if (supplied && flags == (E ? 15U : 7U) && *max_element(e.begin(), e.end()) == 3) {
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
          // Floyd transitive closure is independent of the per-source queue BFS.
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
          if (connected) {
            ++sc;
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
    return result;
  }
  static bool compatible(const Action &action, const vector<int> &e) {
    for (size_t u = 0; u < e.size(); ++u) {
      int v = action.pair[u];
      if ((action.forced >> u & 1) && e[u] != 3)
        return false;
      if (v == -1 && e[u] != 1)
        return false;
      if (v >= 0 && e[u] > 1 + e[v])
        return false;
    }
    return true;
  }
  void derive_extensions(const vector<int> &e) {
    if (E || !(B & C))
      return;
    // All survivors happen to have H3 generated by a and the path 3-0-1-4,
    // or its 1<->2 image. Check this before using its Boolean completion.
    assert(core.id == 7 && D == 9);
    int middle = __builtin_ctz(unsigned((B | C) & ~17));
    vector<int> old = {1 << core.n, B, C, D, 24}; // 24 mask = pair 34, not edge 24.
    assert(middle == 1 || middle == 2);
    for (const auto &f : raw_maps)
      if (compatible(profile(f), e)) {
        unsigned pre = 0;
        for (int q = 0; q < int(f.size()); ++q)
          if (D >> f[q] & 1)
            pre |= 1U << q;
        if (find(old.begin(), old.end(), int(pre)) != old.end())
          continue;
        // A new actual preimage is a short one-count clique. These are necessary
        // consequences of arrival within four steps and safety through eleven.
        if (!pre || (__builtin_popcount(pre) == 1 && __builtin_ctz(pre) < core.n))
          continue;
        bool allowed = true;
        for (int mask : old)
          if (pre != unsigned(mask) && ((pre & mask) == pre || (pre & mask) == unsigned(mask)))
            allowed = false;
        for (auto [u, v] : long_pairs)
          if ((pre >> u & 1) && (pre >> v & 1))
            allowed = false;
        if (!allowed)
          continue;
        int outside = 0, normalized = pre & ((1 << fixed()) - 1);
        for (int q = fixed(); q < int(f.size()); ++q)
          if (pre >> q & 1) {
            ++outside;
            normalized |= 1 << fixed();
          }
        // These assertions are exhaustive domain results, not generator pruning.
        assert(outside <= 1 && __builtin_popcount(pre) <= 2);
        extensions.insert(normalized);
      }
    // H4 strictly extends H3, so at least one of these actual preimages must
    // occur in any real alphabet. Fourth-stage jobs are generated from this set.
  }
  string run() {
    generate();
    check_kernel();
    distances();
    ostringstream out;
    unsigned allflags = 0;
    for (auto m : marks)
      allflags |= m.flags;
    out << "T=" << core.id << " Bmask=" << B << " Cmask=" << C << " Dmask=" << D << " Emask=" << E
        << " allflags=" << allflags << " domain=" << domains << " kernel_domain=" << kernel_domains
        << " signatures=" << signature_count << " invalid_P1=" << invalid_p1 << " joint=" << joint
        << " SC=" << sc << '\n';
    for (const auto &e : survivor_vectors) {
      out << "SC_vector";
      for (int x : e)
        out << ' ' << x;
      out << '\n';
    }
    if (!extensions.empty()) {
      out << "FOURTH";
      for (int mask : extensions)
        out << ' ' << mask;
      out << '\n';
    }
    return out.str();
  }
};
void controls() {
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
  vector<int> identity(13);
  iota(identity.begin(), identity.end(), 0);
  vector<int> collapse(13, 0);
  for (bool exact : {false, true}) {
    assert(trial.safe_rank(identity, 9, 8, exact));
    assert(trial.safe_rank(identity, 10, 3, exact));
    assert(!trial.safe_rank(collapse, 9, 8, exact));
    assert(!trial.safe_rank(collapse, 10, 3, exact));
  }
  // Exact equality of retained literal-map sets also checks rejection decisions
  // between the two generators and rank methods; no stored records are read.
  cout << "CONTROLS positive/negative distance, rank, and nonedge constraints PASS" << endl;
}
int main(int argc, char **argv) {
  controls();
  int threads = 4;
  bool disjoint = false;
  for (int i = 1; i < argc; ++i) {
    if (string(argv[i]) == "--disjoint")
      disjoint = true;
    else if (string(argv[i]) == "--threads" && i + 1 < argc)
      threads = stoi(argv[++i]);
    else
      return 2;
  }
  if (threads < 1 || threads > 32)
    return 2;
  struct Job {
    Core core;
    int B, C, D, E;
  };
  vector<Job> jobs;
  for (auto core : cores) {
    vector<int> edges;
    istringstream input(core.text);
    string edge;
    while (input >> edge)
      edges.push_back((1 << (edge[0] - '0')) | (1 << (edge[1] - '0')));
    for (int B : edges)
      for (int C : edges)
        if (B != C && __builtin_popcount(unsigned(B & C)) == (disjoint ? 0 : 1)) {
          auto third = edges;
          third.push_back(1 << (core.n + 1));
          for (int D : third)
            if (D != B && D != C) {
              Case trial(core, B, C, D);
              if (trial.prepare())
                jobs.push_back({core, B, C, D, 0});
            }
        }
  }
  if (!disjoint)
    assert(jobs.size() == 276);
  auto stage = [&](const vector<Job> &domain, vector<Job> &next_jobs) {
    atomic<int> next{0}, complete{0};
    atomic<uint64_t> total_sc{0};
    mutex output;
    vector<thread> workers;
    for (int t = 0; t < threads; ++t)
      workers.emplace_back([&] {
        for (int j; (j = next.fetch_add(1)) < int(domain.size());) {
          auto job = domain[j];
          Case trial(job.core, job.B, job.C, job.D, job.E);
          assert(trial.prepare());
          string result = trial.run();
          total_sc.fetch_add(trial.sc);
          ++complete;
          lock_guard<mutex> guard(output);
          cout << result << flush;
          for (int E : trial.extensions)
            next_jobs.push_back({job.core, job.B, job.C, job.D, E});
        }
      });
    for (auto &worker : workers)
      worker.join();
    assert(complete == int(domain.size()));
    cout << "COMPLETE cases=" << complete << " requested=" << domain.size()
         << " SC_total=" << total_sc << endl;
    return total_sc.load();
  };
  vector<Job> fourth, unused;
  uint64_t third_survivors = stage(jobs, fourth);
  if (disjoint) {
    cout << "RESTRICTED disjoint triangle-free tau2 third-layer domain; other cores and singleton "
            "first/second entries are outside scope"
         << endl;
    return third_survivors ? 3 : 0;
  }
  assert(third_survivors == 4 && fourth.size() == 20);
  uint64_t survivors = stage(fourth, unused);
  assert(unused.empty());
  return survivors ? 3 : 0;
}
