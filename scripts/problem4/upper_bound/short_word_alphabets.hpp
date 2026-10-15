// Necessary arbitrary-alphabet short-word compatibility relaxation.
// PROOF.md#problem4-full-fiber-flag. No alphabet-size cutoff is imposed.
#pragma once
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <functional>
#include <map>
#include <utility>
#include <vector>
struct ShortWordCliqueResult {
  bool possible = false;
  int groups = 0;
  uint64_t nodes = 0, pair_checks = 0;
  std::vector<int> witness;
};
struct AvoidanceClosure {
  bool avoids = false;
  std::vector<unsigned> sets;
  std::vector<unsigned char> seen;
};
inline unsigned literal_preimage(unsigned set, const std::vector<int>& f) {
  unsigned pre = 0;
  for (int q = 0; q < int(f.size()); ++q)
    if (set >> f[q] & 1) pre |= 1U << q;
  return pre;
}
inline AvoidanceClosure full_avoidance_closure(
    int n, int protected_point, const std::vector<std::vector<int>>& letters,
    const std::vector<int>& selected) {
  AvoidanceClosure answer;
  answer.seen.resize(1U << n);
  answer.sets.push_back(1U << protected_point);
  answer.seen[answer.sets.front()] = 1;
  for (size_t at = 0; at < answer.sets.size(); ++at)
    for (int i : selected) {
      unsigned pre = literal_preimage(answer.sets[at], letters[i]);
      if (!pre) {answer.avoids = true;return answer;}
      if (!answer.seen[pre]) {
        answer.seen[pre] = 1;answer.sets.push_back(pre);
      }
    }
  return answer;
}
struct ExpandedReachabilityClosure {
  bool reached = false;
  std::vector<unsigned> states;
  std::vector<unsigned char> seen;
};
// State = external mask | (number of missing protected states << q).
// The retained block has defect points (defect>=2). Relative to defect+1,
// the only lost legal transitions are permutation self-loops at full external
// occupancy and defect missing protected states; reachability is unchanged.
inline std::vector<unsigned> expanded_successors(
    int q, int defect, unsigned state, const std::vector<int>& f) {
  unsigned mask=state&((1U<<q)-1),outside=0;
  int absent=state>>q,hits=0,exported=f[q]!=q;
  for(int x=0;x<q;++x) if(mask>>x&1) {
    if(f[x]==q) hits=1;else outside|=1U<<f[x];
  }
  std::vector<unsigned> next;
  for(int occupied=0;occupied<=exported;++occupied) {
    if(occupied>defect-absent||exported-occupied>absent) continue;
    unsigned image=outside|(occupied?(1U<<f[q]):0);
    int missing=absent+occupied-hits;
    assert(missing>=0);
    if(missing+q-__builtin_popcount(image)<=defect)
      next.push_back(image|(unsigned(missing)<<q));
  }
  return next;
}
inline ExpandedReachabilityClosure expanded_reachability_closure(
    int q, unsigned target, const std::vector<std::vector<int>>& letters,
    const std::vector<int>& selected) {
  int defect=q-__builtin_popcount(target);
  assert(target&&target<(1U<<q)&&defect>=2);
  ExpandedReachabilityClosure answer;
  answer.seen.resize((defect+1)*(1U<<q));
  answer.states.push_back((1U<<q)-1);answer.seen[answer.states.front()]=1;
  for(size_t at=0;at<answer.states.size();++at) for(int f:selected)
    for(unsigned next:expanded_successors(q,defect,answer.states[at],letters[f])) {
      if(next==target) {answer.reached=true;return answer;}
      if(!answer.seen[next]) {answer.seen[next]=1;answer.states.push_back(next);}
    }
  return answer;
}
template<int n = 13>
inline ShortWordCliqueResult
short_word_clique(const std::vector<std::vector<int>> &letters,
                  const std::vector<unsigned> &supplies, unsigned required,
                  int protected_point,
                  const std::vector<std::pair<unsigned, int>> &seeds,
                  const std::vector<std::pair<int, int>> &edges,
                  const std::vector<int> &distances, bool fold = true,
                  bool require_full_avoidance = false,
                  unsigned expanded_target = 0) {
  using namespace std;
  const int raw_count = letters.size();
  static_assert(n >= 13 && n <= 14);
  constexpr int masks = 1 << n;
  for (const auto& row : letters) assert(row.size() == n);
  if(expanded_target) {
    assert(protected_point==n-1&&(expanded_target>>(n-1)&1));
    assert(__builtin_popcount(expanded_target)==n-4&&require_full_avoidance);
    for(const auto& f:letters) {
      assert(find(f.begin(),f.end(),n-1)!=f.end());
      for(int x=0;x<n-1;++x) assert(f[x]!=f[n-1]);
    }
  }
  int count = raw_count;
  ShortWordCliqueResult result;
  vector<array<uint16_t, masks>> images(count);
  for (int i = 0; i < count; ++i) {
    images[i][0] = 0;
    for (unsigned mask = 1; mask < masks; ++mask) {
      unsigned low = mask & -mask;
      int q = __builtin_ctz(low);
      images[i][mask] = images[i][mask ^ low] | (1U << letters[i][q]);
    }
  }
  auto safe = [&](unsigned mask, int left) {
    if (__builtin_popcount(mask) != n - 4 || !(mask >> protected_point & 1))
      return false;
    for (size_t i = 0; i < edges.size(); ++i)
      if (distances[i] <= left) {
        auto [u, v] = edges[i];
        if ((mask >> u & 1) && (mask >> v & 1))
          return false;
      }
    return true;
  };
  // Finite-horizon behavioral equivalence. States are (subset, remaining
  // budget); failure is class zero. Equal classes accept the same suffixes
  // over the entire raw alphabet. Equivalent letters may all be added together
  // without creating a bad short word, so their suppliers and state arrows
  // can be united without imposing any alphabet-size bound.
  int horizon = 0;
  for (auto seed : seeds)
    horizon = max(horizon, seed.second);
  vector<array<bool, masks>> active(horizon + 1);
  vector<pair<unsigned, int>> work;
  for (auto [mask, left] : seeds)
    if (!active[left][mask]) {
      active[left][mask] = true;
      work.push_back({mask, left});
    }
  for (size_t at = 0; at < work.size(); ++at) {
    auto [mask, left] = work[at];
    if (!left || !safe(mask, left))
      continue;
    for (int f = 0; f < raw_count; ++f) {
      unsigned out = images[f][mask];
      if (safe(out, left - 1) && !active[left - 1][out]) {
        active[left - 1][out] = true;
        work.push_back({out, left - 1});
      }
    }
  }
  vector<array<int, masks>> classes(horizon + 1);
  for (unsigned mask = 0; mask < masks; ++mask)
    if (active[0][mask] && safe(mask, 0))
      classes[0][mask] = 1;
  for (int left = 1; left <= horizon; ++left) {
    map<vector<int>, int> labels;
    for (unsigned mask = 0; mask < masks; ++mask)
      if (active[left][mask] && safe(mask, left)) {
        vector<int> signature;
        signature.reserve(raw_count);
        for (int f = 0; f < raw_count; ++f)
          signature.push_back(classes[left - 1][images[f][mask]]);
        auto found = labels.find(signature);
        if (found == labels.end())
          found = labels.emplace(move(signature), labels.size() + 1).first;
        classes[left][mask] = found->second;
      }
  }
  map<vector<int>, vector<int>> equivalent;
  for (int f = 0; f < raw_count; ++f) {
    vector<int> signature;
    for (int left = 1; left <= horizon; ++left)
      for (unsigned mask = 0; mask < masks; ++mask)
        if (active[left][mask] && safe(mask, left))
          signature.push_back(classes[left - 1][images[f][mask]]);
    if (!fold)
      signature.push_back(f);
    equivalent[signature].push_back(f);
  }
  vector<int> representative;
  vector<vector<int>> members;
  vector<unsigned> group_supplies;
  vector<array<unsigned, n>> group_graph;
  for (const auto &entry : equivalent) {
    members.push_back(entry.second);
    representative.push_back(entry.second.front());
    unsigned flags = 0;
    array<unsigned, n> graph{};
    for (int f : entry.second) {
      flags |= supplies[f];
      for (int q = 0; q < n; ++q)
        graph[q] |= 1U << letters[f][q];
    }
    group_supplies.push_back(flags);
    group_graph.push_back(graph);
  }
  count = members.size();
  result.groups = count;
  vector<int8_t> compatible(count * count, -1);
  auto pair_safe = [&](int x, int y) {
    int8_t &answer = compatible[x * count + y];
    if (answer >= 0)
      return bool(answer);
    ++result.pair_checks;
    array<int8_t, masks> best;
    best.fill(-1);
    vector<pair<unsigned, int>> todo;
    for (auto [mask, left] : seeds)
      if (best[mask] < left) {
        best[mask] = left;
        todo.push_back({mask, left});
      }
    bool valid = true;
    for (size_t at = 0; at < todo.size() && valid; ++at) {
      auto [mask, left] = todo[at];
      if (!safe(mask, left)) {
        valid = false;
        break;
      }
      if (!left || best[mask] > left)
        continue;
      for (int f : {x, y}) {
        unsigned out = images[representative[f]][mask];
        if (best[out] < left - 1) {
          best[out] = left - 1;
          todo.push_back({out, left - 1});
        }
      }
    }
    answer = valid;
    compatible[y * count + x] = valid;
    return valid;
  };
  auto jointly_safe = [&](const vector<int> &chosen) {
    array<int8_t, masks> best;
    best.fill(-1);
    vector<pair<unsigned, int>> todo;
    for (auto [mask, left] : seeds)
      if (best[mask] < left) {
        best[mask] = left;
        todo.push_back({mask, left});
      }
    for (size_t at = 0; at < todo.size(); ++at) {
      auto [mask, left] = todo[at];
      if (!safe(mask, left))
        return false;
      if (!left || best[mask] > left)
        continue;
      for (int f : chosen) {
        unsigned out = images[representative[f]][mask];
        if (best[out] < left - 1) {
          best[out] = left - 1;
          todo.push_back({out, left - 1});
        }
      }
    }
    return true;
  };
  vector<int> available, selected;
  for (int i = 0; i < count; ++i)
    if (pair_safe(i, i))
      available.push_back(i);
  function<bool(vector<int>, unsigned)> search = [&](vector<int> pool,
                                                     unsigned covered) {
    ++result.nodes;
    unsigned total = covered;
    for (int i : pool)
      total |= group_supplies[i];
    if ((total & required) != required)
      return false;
    vector<int> clause;
    bool need = false;
    auto choose = [&](vector<int> next) {
      if (!need || next.size() < clause.size())
        clause = move(next);
      need = true;
    };
    for (unsigned bits = required & ~covered; bits; bits &= bits - 1) {
      unsigned bit = bits & -bits;
      vector<int> next;
      for (int i : pool)
        if (group_supplies[i] & bit)
          next.push_back(i);
      choose(move(next));
    }
    array<unsigned, n> reach{};
    for (int q = 0; q < n; ++q)
      reach[q] = 1U << q;
    for (int i : selected)
      for (int q = 0; q < n; ++q)
        reach[q] |= group_graph[i][q];
    for (int k = 0; k < n; ++k)
      for (int q = 0; q < n; ++q)
        if (reach[q] >> k & 1)
          reach[q] |= reach[k];
    for (int q = 0; q < n; ++q)
      if (reach[q] != masks - 1) {
        vector<int> next;
        unsigned from = reach[q];
        for (int i : pool) {
          bool leaves = false;
          for (int u = 0; u < n; ++u)
            if ((from >> u & 1) && (group_graph[i][u] & ~from))
              leaves = true;
          if (leaves)
            next.push_back(i);
        }
        if (next.empty())
          return false;
        choose(move(next));
      }
    if (!need && require_full_avoidance) {
      vector<int> chosen_letters;
      for (int g : selected)
        chosen_letters.insert(chosen_letters.end(), members[g].begin(), members[g].end());
      auto closure = full_avoidance_closure(n, protected_point, letters, chosen_letters);
      if (!closure.avoids) {
        vector<int> next;
        for (int g : pool) {
          bool leaves = false;
          for (int f : members[g]) for (unsigned set : closure.sets)
            if (!closure.seen[literal_preimage(set, letters[f])]) {leaves = true;break;}
          if (leaves) next.push_back(g);
        }
        // If every remaining letter preserves this nonempty preimage family,
        // no extension can avoid the protected state from the full state set.
        if (next.empty()) return false;
        choose(move(next));
      }
    }
    if(!need&&expanded_target) {
      vector<int> chosen_letters;
      for(int g:selected)
        chosen_letters.insert(chosen_letters.end(),members[g].begin(),members[g].end());
      unsigned target=expanded_target&((1U<<(n-1))-1);
      auto closure=expanded_reachability_closure(n-1,target,letters,chosen_letters);
      if(!closure.reached) {
        vector<int> next;
        int defect=n-1-__builtin_popcount(target);
        for(int g:pool) {
          bool leaves=false;
          for(int f:members[g]) for(unsigned state:closure.states)
            for(unsigned image:expanded_successors(n-1,defect,state,letters[f]))
              if(!closure.seen[image]) leaves=true;
          if(leaves) next.push_back(g);
        }
        if(next.empty()) return false;
        choose(move(next));
      }
    }
    if (!need) {
      result.witness.clear();
      for (int g : selected)
        result.witness.insert(result.witness.end(), members[g].begin(),
                              members[g].end());
      return true;
    } // Synchronization is not assumed.
    if (clause.empty())
      return false;
    stable_sort(clause.begin(), clause.end(), [&](int a, int b) {
      return __builtin_popcount(group_supplies[a] & ~covered) >
             __builtin_popcount(group_supplies[b] & ~covered);
    });
    for (int i : clause) {
      auto found = find(pool.begin(), pool.end(), i);
      if (found == pool.end())
        continue;
      pool.erase(
          found); // Later branches omit all earlier members of this clause.
      selected.push_back(i);
      if (selected.size() > 2 && !jointly_safe(selected)) {
        selected.pop_back();
        continue;
      }
      vector<int> next;
      for (int j : pool)
        if (pair_safe(i, j))
          next.push_back(j);
      bool possible = search(move(next), covered | group_supplies[i]);
      selected.pop_back();
      if (possible)
        return true;
    }
    return false;
  };
  result.possible = search(move(available), 0);
  return result;
}
template<int n = 13>
inline void short_word_clique_controls() {
  using namespace std;
  constexpr unsigned initial = (1U << (n - 4)) - 1;
  constexpr unsigned full = (1U << n) - 1;
  for (int variant : {0, 1}) {
    vector<vector<int>> universe;
    for (int shift : {0, 1, n - 1, 2, n - 2, 3, n - 3}) {
      vector<int> f(n);
      for (int q = 0; q < n; ++q)
        f[q] = (q + shift) % n;
      universe.push_back(f);
    }
    universe.push_back(vector<int>(n, 0));
    if (variant == 1) {
      for (int q = 0; q < n; ++q)
        universe[3][q] = (n - 5 - q + n) % n;
      for (int i : {4, 5}) {
        for (int q = 0; q < n; ++q)
          universe[i][q] = q;
        swap(universe[i][i == 4 ? 1 : 4], universe[i][i == 4 ? n - 4 : n - 3]);
      }
    }
    vector<pair<int, int>> core_edges =
        variant == 0 ? vector<pair<int, int>>{}
                     : vector<pair<int, int>>{{n - 4, n - 2}, {n - 3, n - 1}};
    vector<int> lengths = variant == 0 ? vector<int>{} : vector<int>{1, 2};
    auto literal_safe = [&](unsigned mask, int left) {
      if (__builtin_popcount(mask) != n - 4 || !(mask & 8))
        return false;
      for (size_t i = 0; i < core_edges.size(); ++i) {
        auto [u, v] = core_edges[i];
        if (lengths[i] <= left && (mask >> u & 1) && (mask >> v & 1))
          return false;
      }
      return true;
    };
    constexpr unsigned start = initial, required = 7;
    auto literal_image = [](unsigned mask, const vector<int> &f) {
      unsigned out = 0;
      for (int q = 0; q < n; ++q)
        if (mask >> q & 1)
          out |= 1U << f[q];
      return out;
    };
    bool pair_ok[8][8]{};
    for (int i = 0; i < 8; ++i)
      for (int j = 0; j < 8; ++j) {
        vector<unsigned> frontier{start};
        bool safe = true;
        for (int length = 0; length <= 3; ++length) {
          vector<unsigned> next;
          for (unsigned mask : frontier) {
            if (!literal_safe(mask, 3 - length))
              safe = false;
            if (length < 3)
              for (int f : {i, j})
                next.push_back(literal_image(mask, universe[f]));
          }
          frontier = move(next);
        }
        pair_ok[i][j] = safe;
      }
    array<bool, 256> valid{};
    for (unsigned selected = 1; selected < 256; ++selected) {
      unsigned supply = 0;
      bool clique = true;
      for (int i = 0; i < 8; ++i)
        if (selected >> i & 1) {
          supply |= 1U << (i % 3);
          for (int j = 0; j < 8; ++j)
            if ((selected >> j & 1) && !pair_ok[i][j])
              clique = false;
        }
      if (!clique || supply != required)
        continue;
      bool sc = true;
      for (int start_state = 0; start_state < n; ++start_state) {
        unsigned visited = 1U << start_state;
        vector<int> queue{start_state};
        for (size_t at = 0; at < queue.size(); ++at)
          for (int f = 0; f < 8; ++f)
            if (selected >> f & 1) {
              int out = universe[f][queue[at]];
              if (!(visited >> out & 1)) {
                visited |= 1U << out;
                queue.push_back(out);
              }
            }
        sc &= visited == full;
      }
      vector<unsigned> frontier{start};
      bool safe = true;
      for (int length = 0; length <= 3; ++length) {
        vector<unsigned> next;
        for (unsigned mask : frontier) {
          if (!literal_safe(mask, 3 - length))
            safe = false;
          if (length < 3)
            for (int f = 0; f < 8; ++f)
              if (selected >> f & 1)
                next.push_back(literal_image(mask, universe[f]));
        }
        frontier = move(next);
      }
      valid[selected] = sc && safe;
    }
    int positives = 0, negatives = 0;
    for (unsigned pool = 0; pool < 256; ++pool) {
      bool reference = false;
      for (unsigned selected = pool; selected; selected = (selected - 1) & pool)
        reference |= valid[selected];
      vector<vector<int>> letters;
      vector<unsigned> flags;
      for (int i = 0; i < 8; ++i)
        if (pool >> i & 1) {
          letters.push_back(universe[i]);
          flags.push_back(1U << (i % 3));
        }
      for (bool fold : {false, true}) {
        auto answer =
            short_word_clique<n>(letters, flags, required, 3, {{start, 3}},
                              core_edges, lengths, fold);
        assert(answer.possible == reference);
      }
      reference ? ++positives : ++negatives;
    }
    assert(positives > 0 && negatives > 0);
  }
  // Three noncommuting permutations are pairwise safe, but their mixed word
  // abc omits the protected point. Their union is strongly connected and all
  // three supply bits are necessary, so pair tests alone would accept them.
  vector<vector<int>> triple(3, vector<int>(n));
  for (auto &f : triple)
    for (int q = 0; q < n; ++q)
      f[q] = q;
  swap(triple[0][0], triple[0][n - 4]);
  swap(triple[1][0], triple[1][1]);
  vector<int> cycle;
  for (int q = 2; q < n; ++q) if (q != 3) cycle.push_back(q);
  for (size_t q = 0; q < cycle.size(); ++q)
    triple[1][cycle[q]] = cycle[(q + 1) % cycle.size()];
  swap(triple[2][1], triple[2][3]);
  for (int x = 0; x < 3; ++x)
    for (int y = 0; y < 3; ++y) {
      vector<unsigned> frontier{initial};
      for (int d = 0; d <= 3; ++d) {
        vector<unsigned> next;
        for (unsigned mask : frontier) {
          assert(mask & 8);
          for (int f : {x, y}) {
            unsigned out = 0;
            for (int q = 0; q < n; ++q)
              if (mask >> q & 1)
                out |= 1U << triple[f][q];
            next.push_back(out);
          }
        }
        frontier = move(next);
      }
    }
  unsigned bad = initial;
  for (const auto &f : triple) {
    unsigned next = 0;
    for (int q = 0; q < n; ++q)
      if (bad >> q & 1)
        next |= 1U << f[q];
    bad = next;
  }
  assert(!(bad & 8));
  for (int start = 0; start < n; ++start) {
    vector<int> queue{start};
    unsigned seen = 1U << start;
    for (size_t i = 0; i < queue.size(); ++i)
      for (const auto &f : triple) {
        int v = f[queue[i]];
        if (!(seen >> v & 1)) {
          seen |= 1U << v;
          queue.push_back(v);
        }
      }
    assert(seen == full);
  }
  for (bool fold : {false, true})
    assert(!short_word_clique<n>(triple, {1, 2, 4}, 7, 3, {{initial, 3}}, {}, {}, fold)
                .possible);
}

// Independent forward-image controls for the full-state avoidance extension.
template<int n = 14>
inline void short_word_avoidance_controls() {
  using namespace std;
  auto forward_avoids = [](int width, int a, const vector<vector<int>>& maps,
                           const vector<int>& alphabet) {
    vector<unsigned char> seen(1U << width);
    vector<unsigned> todo{(1U << width)-1};seen[todo.front()]=1;
    for(size_t at=0;at<todo.size();++at) for(int f:alphabet) {
      unsigned image=0;
      for(int q=0;q<width;++q) if(todo[at]>>q&1) image|=1U<<maps[f][q];
      if(!(image>>a&1)) return true;
      if(!seen[image]) {seen[image]=1;todo.push_back(image);}
    }
    return false;
  };
  vector<vector<int>> small;
  for(int code=0;code<27;++code) {
    int rest=code;vector<int> f(3);
    for(int& q:f) {q=rest%3;rest/=3;}small.push_back(f);
  }
  int cut_checks=0;
  for(int f=0;f<27;++f) for(int g=0;g<27;++g) for(int a=0;a<3;++a) {
    auto closure=full_avoidance_closure(3,a,small,{f});
    auto both=full_avoidance_closure(3,a,small,{f,g});
    assert(closure.avoids==forward_avoids(3,a,small,{f}));
    assert(both.avoids==forward_avoids(3,a,small,{f,g}));
    if(!closure.avoids) {
      bool leaves=false;
      for(unsigned set:closure.sets) leaves|=!closure.seen[literal_preimage(set,small[g])];
      if(both.avoids) assert(leaves);
      if(!leaves) assert(!both.avoids);
    }
    ++cut_checks;
  }
  vector<vector<int>> universe(6,vector<int>(n));
  for(int q=0;q<n;++q) {
    universe[0][q]=(q+1)%n;
    universe[1][q]=q==n-1?0:q;
    universe[2][q]=q;
    universe[3][q]=(q+n-1)%n;
    universe[4][q]=q==0?n-1:(q==n-1?0:q);
    universe[5][q]=0;
  }
  constexpr unsigned initial=(1U<<(n-4))-1,full=(1U<<n)-1;
  array<bool,64> valid{};int positives=0,negatives=0;
  for(unsigned subset=1;subset<64;++subset) {
    vector<int> alphabet;unsigned flags=0;
    for(int f=0;f<6;++f) if(subset>>f&1) {alphabet.push_back(f);flags|=1U<<(f%2);}
    if(flags!=3) continue;
    bool sc=true;
    for(int start=0;start<n;++start) {
      unsigned visited=1U<<start;vector<int> todo{start};
      for(size_t at=0;at<todo.size();++at) for(int f:alphabet) {
        int out=universe[f][todo[at]];
        if(!(visited>>out&1)) {visited|=1U<<out;todo.push_back(out);}
      }
      sc&=visited==full;
    }
    if(!sc) continue;
    vector<unsigned> frontier{initial};bool safe=true;
    for(int length=1;length<=3&&safe;++length) {
      vector<unsigned> next;
      for(unsigned mask:frontier) for(int f:alphabet) {
        unsigned image=0;for(int q=0;q<n;++q) if(mask>>q&1) image|=1U<<universe[f][q];
        if(__builtin_popcount(image)!=n-4||!(image&8)) safe=false;
        next.push_back(image);
      }
      frontier=move(next);
    }
    valid[subset]=safe&&forward_avoids(n,3,universe,alphabet);
  }
  assert(valid[3]); // cycle plus the unit merge is a positive control
  assert(!valid[9]); // strongly connected permutations cannot avoid from Q
  for(unsigned pool=0;pool<64;++pool) {
    bool expected=false;
    for(unsigned subset=pool;subset;subset=(subset-1)&pool) expected|=valid[subset];
    vector<vector<int>> letters;vector<unsigned> flags;
    for(int f=0;f<6;++f) if(pool>>f&1) {letters.push_back(universe[f]);flags.push_back(1U<<(f%2));}
    for(bool fold:{false,true}) {
      auto answer=short_word_clique<n>(letters,flags,3,3,{{initial,3}},{},{},fold,true);
      assert(answer.possible==expected);
      if(answer.possible) assert(forward_avoids(n,3,letters,answer.witness));
    }
    expected?++positives:++negatives;
  }
  assert(positives&&negatives&&cut_checks==2187);
  // These letters are indistinguishable within the three-step safe horizon,
  // but only the nonrepresentative merge permits eventual avoidance from Q.
  vector<vector<int>> folded{universe[0],universe[2],universe[1]};
  auto answer=short_word_clique<n>(folded,{1,2,2},3,3,{{initial,3}},{},{},true,true);
  assert(answer.possible&&answer.groups==1);
  assert(forward_avoids(n,3,folded,answer.witness));
}

// Full-subset searches in the expanded automata independently check both the
// quotient transitions and the alphabet-search reachability clauses.
template<int n = 14>
inline void expanded_reachability_controls() {
  using namespace std;
  constexpr int q=n-1;
  constexpr unsigned source=((1U<<n)-1)^15,external=(1U<<q)-1;
  vector<vector<int>> universe(6,vector<int>(n));
  for(int x=0;x<n;++x) {
    universe[0][x]=(x+1)%n;
    universe[1][x]=x==1?2:x;
    universe[2][x]=x;
    universe[3][x]=(x+n-1)%n;
    universe[4][x]=x==1?q:(x==q?1:x);
    universe[5][x]=x==2?1:x;
  }
  auto image=[](unsigned mask,const vector<int>& f) {
    unsigned out=0;for(int x=0;x<int(f.size());++x) if(mask>>x&1) out|=1U<<f[x];return out;
  };
  auto expanded_literal=[&](const vector<int>& alphabet,int retained=4) {
    int width=q+retained;
    unsigned target=(source&external)|(((1U<<retained)-1)<<q);
    vector<vector<int>> expanded;
    for(int i:alphabet) {
      vector<int> f(width);for(int x=0;x<width;++x) f[x]=x;
      for(int x=0;x<q;++x) f[x]=universe[i][x];f[q]=universe[i][q];
      expanded.push_back(move(f));
    }
    // Adjacent protected transpositions generate every independent rewiring
    // through composition before and after each canonical expanded letter.
    for(int i=q;i<width-1;++i) {
      vector<int> f(width);for(int x=0;x<width;++x) f[x]=x;swap(f[i],f[i+1]);expanded.push_back(move(f));
    }
    vector<unsigned char> seen(1U<<width);vector<unsigned> todo{(1U<<width)-1};seen[todo[0]]=1;
    for(size_t at=0;at<todo.size();++at) for(const auto& f:expanded) {
      unsigned out=image(todo[at],f);
      if(out==target) return true;
      if(__builtin_popcount(out)>=width-4&&!seen[out]) {seen[out]=1;todo.push_back(out);}
    }
    return false;
  };
  auto full_avoids=[&](const vector<int>& alphabet) {
    vector<unsigned char> seen(1U<<n);vector<unsigned> todo{(1U<<n)-1};seen[todo[0]]=1;
    for(size_t at=0;at<todo.size();++at) for(int i:alphabet) {
      unsigned out=image(todo[at],universe[i]);
      if(!(out>>q&1)) return true;
      if(!seen[out]) {seen[out]=1;todo.push_back(out);}
    }
    return false;
  };
  array<bool,64> valid{};
  for(unsigned subset=0;subset<64;++subset) {
    vector<int> alphabet;unsigned supplies=0;
    for(int f=0;f<6;++f) if(subset>>f&1) {alphabet.push_back(f);supplies|=1U<<(f%2);}
    bool reaches=expanded_literal(alphabet);
    assert(reaches==expanded_literal(alphabet,5));
    assert(expanded_reachability_closure(q,source&external,universe,alphabet).reached==reaches);
    bool sc=true;
    for(int start=0;start<n;++start) {
      unsigned visited=1U<<start;vector<int> todo{start};
      for(size_t at=0;at<todo.size();++at) for(int f:alphabet) {
        int out=universe[f][todo[at]];
        if(!(visited>>out&1)) {visited|=1U<<out;todo.push_back(out);}
      }
      sc&=visited==(1U<<n)-1;
    }
    bool safe=true;vector<unsigned> frontier{source};
    for(int length=1;length<=3&&safe;++length) {
      vector<unsigned> next;
      for(unsigned mask:frontier) for(int f:alphabet) {
        unsigned out=image(mask,universe[f]);
        if(__builtin_popcount(out)!=n-4||!(out>>q&1)) safe=false;
        next.push_back(out);
      }
      frontier=move(next);
    }
    valid[subset]=supplies==3&&sc&&safe&&reaches&&full_avoids(alphabet);
  }
  assert(valid[3]);
  int positives=0,negatives=0;
  for(unsigned pool=0;pool<64;++pool) {
    bool expected=false;
    for(unsigned subset=pool;subset;subset=(subset-1)&pool) expected|=valid[subset];
    vector<vector<int>> maps;vector<unsigned> flags;
    for(int i=0;i<6;++i) if(pool>>i&1) {maps.push_back(universe[i]);flags.push_back(1U<<(i%2));}
    for(bool fold:{false,true}) {
      auto answer=short_word_clique<n>(maps,flags,3,q,{{source,3}},{},{},fold,true,source);
      assert(answer.possible==expected);
      if(answer.possible) {
        vector<int> alphabet;
        for(int local:answer.witness) {
          int i=find(universe.begin(),universe.end(),maps[local])-universe.begin();
          assert(i<6);alphabet.push_back(i);
        }
        assert(expanded_literal(alphabet)&&full_avoids(alphabet));
      }
    }
    expected?++positives:++negatives;
  }
  assert(positives&&negatives);
  for(int f=0;f<6;++f) for(int g=0;g<6;++g) {
    auto one=expanded_reachability_closure(q,source&external,universe,{f});
    auto both=expanded_reachability_closure(q,source&external,universe,{f,g});
    if(!one.reached&&both.reached) {
      bool leaves=false;
      for(unsigned state:one.states) for(unsigned out:expanded_successors(q,4,state,universe[g]))
        leaves|=!one.seen[out];
      assert(leaves);
    }
  }
}
