// Exhaustive integer compatibility check; see
// proofs/paper/problem4_c7_sixth_layer.md. Reads complete literal action rows
// produced by problem4_c7_profiles.cpp.
#include <algorithm>
#include <array>
#include <iostream>
#include <set>
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
int main() {
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
  long long dn = 0, retained = 0, joint = 0, tested = 0;
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
    for (int ec = 0; ec < 279936; ec++) {
      array<int, 7> e;
      int y = ec;
      for (int i = 0; i < 7; i++) {
        e[i] = 1 + y % 6;
        y /= 6;
      }
      tested++;
      if (certified(pool, d, e)) {
        joint++;
      }
    }
  }
  cout << "subset vectors " << dn << " candidates " << retained
       << " joint vectors " << tested << " survivors " << joint << endl;
  return (joint || dn != 3960 || retained != 14 || tested != 3919104) ? 1 : 0;
}
