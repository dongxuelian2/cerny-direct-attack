// Exhaustive integer compatibility check; see
// PROOF.md#problem4-problem4-c7-sixth-layer. Reads complete literal action rows
// produced by problem4_c7_profiles.cpp.
#include <algorithm>
#include <atomic>
#include <array>
#include <iostream>
#include <set>
#include <string>
#include <thread>
#include <vector>
using namespace std;
struct A {
  array<int, 7> p, t;
  int six;
  bool operator<(const A &o) const {
    return p != o.p ? p < o.p : t != o.t ? t < o.t : six < o.six;
  }
};
int edge(int a, int b) {
  if (a == b)
    return -1;
  for (int i = 0; i < 7; i++)
    if ((a == i && b == (i + 1) % 7) || (b == i && a == (i + 1) % 7))
      return i;
  return 7;
}
bool allowed(const A &a, const array<int, 8> &d, const array<int, 7> &e) {
  for (int i = 0; i < 7; i++) {
    if (d[i] > 1 + d[a.p[i]])
      return false;
    if ((a.six >> i & 1) && e[i] != 6)
      return false;
    if (a.t[i] == -1 && e[i] != 1)
      return false;
    if (a.t[i] < 7 && a.t[i] >= 0 && e[i] > 1 + e[a.t[i]])
      return false;
  }
  return true;
}
bool certified(const vector<A> &acts, const array<int, 8> &d,
               const array<int, 7> &e) {
  int ds = 0, es = 0;
  for (auto &a : acts)
    if (allowed(a, d, e))
      for (int i = 0; i < 7; i++) {
        if (d[i] == 1 + d[a.p[i]])
          ds |= 1 << i;
        if (a.t[i] == -1 ? e[i] == 1 : a.t[i] < 7 && e[i] == 1 + e[a.t[i]])
          es |= 1 << i;
      }
  return ds == 127 && es == 127;
}
int main(int argc, char **argv) {
  unsigned threads = 1;
  if (argc == 3 && string(argv[1]) == "--threads") {
    try {
      size_t end = 0;
      string value = argv[2];
      auto parsed = stoul(value, &end);
      if (end != value.size() || !parsed || parsed > 64) return 2;
      threads = unsigned(parsed);
    } catch (...) { return 2; }
  } else if (argc != 1) return 2;
  set<A> unique;
  array<int, 8> f;
  while (cin >> f[0]) {
    for (int i = 1; i < 8; i++)
      cin >> f[i];
    A a;
    for (int &i : a.p)
      cin >> i;
    a.six = 0;
    for (int i = 0; i < 7; i++)
      a.t[i] = edge(f[i], f[(i + 1) % 7]);
    for (int u = 0; u < 8; u++)
      for (int v = u + 1; v < 8; v++)
        if (edge(u, v) == 7) {
          int j = edge(f[u], f[v]);
          if (j >= 0 && j < 7)
            a.six |= 1 << j;
        }
    unique.insert(a);
  }
  vector<A> acts(unique.begin(), unique.end());
  cout << "signatures " << acts.size() << endl;
  if (acts.size() != 896)
    return 3;
  A control;
  control.p = {1, 2, 3, 4, 5, 7, 7};
  control.t = {1, 2, 3, 4, 5, -1, -1};
  control.six = 0;
  array<int, 8> cd = {6, 5, 4, 3, 2, 1, 1, 0};
  array<int, 7> ce = {6, 5, 4, 3, 2, 1, 1};
  if (!certified({control}, cd, ce))
    return 2;
  cout << "artificial chain accepted" << endl;
  long long dn = 0, retained = 0;
  struct Job { array<int, 8> d; vector<A> pool; };
  vector<Job> jobs;
  for (int code = 0; code < 823543; code++) {
    array<int, 8> d;
    int x = code, mask = 0, mx = 0;
    for (int i = 0; i < 7; i++) {
      d[i] = 1 + x % 7;
      x /= 7;
      mask |= 1 << d[i];
      mx = max(mx, d[i]);
    }
    d[7] = 0;
    if (d[0] < 6 || mask != ((1 << (mx + 1)) - 2))
      continue;
    dn++;
    vector<A> pool;
    int suppliers = 0;
    for (auto a : acts) {
      bool ok = true;
      for (int i = 0; i < 7; i++)
        if (d[i] > 1 + d[a.p[i]])
          ok = false;
      if (ok) {
        pool.push_back(a);
        for (int i = 0; i < 7; i++)
          if (d[i] == 1 + d[a.p[i]])
            suppliers |= 1 << i;
      }
    }
    if (suppliers != 127)
      continue;
    retained++;
    cout << "subset vector";
    for (int i = 0; i < 7; i++)
      cout << " " << d[i];
    cout << " map signatures " << pool.size() << endl;
    jobs.push_back({d, std::move(pool)});
  }
  // Partition the literal Cartesian domain into disjoint 4096-element blocks.
  // Every assignment is still checked; output order is independent of threads.
  constexpr int width = 4096, per_vector = 279936;
  constexpr int blocks = (per_vector + width - 1) / width;
  atomic<size_t> next{0};
  atomic<long long> joint{0}, tested{0};
  vector<thread> workers;
  for (unsigned t = 0; t < threads; ++t) workers.emplace_back([&] {
    long long local_joint = 0, local_tested = 0;
    for (size_t task; (task = next.fetch_add(1)) < jobs.size() * blocks;) {
      const auto &job = jobs[task / blocks];
      const int begin = int(task % blocks) * width;
      const int end = min(begin + width, per_vector);
      for (int ec = begin; ec < end; ++ec) {
        array<int, 7> e;
        int y = ec;
        for (int i = 0; i < 7; ++i) { e[i] = 1 + y % 6; y /= 6; }
        ++local_tested;
        if (certified(job.pool, job.d, e)) ++local_joint;
      }
    }
    joint.fetch_add(local_joint); tested.fetch_add(local_tested);
  });
  for (auto &worker : workers) worker.join();
  cout << "subset vectors " << dn << " candidates " << retained
       << " joint vectors " << tested.load() << " survivors " << joint.load() << endl;
  return (joint.load() || dn != 3960 || retained != 14 || tested.load() != 3919104) ? 1 : 0;
}
