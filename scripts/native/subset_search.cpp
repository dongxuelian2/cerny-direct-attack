// Exact forward subset BFS. Independent cases run on disjoint worker threads.
// Input records: reset n k <k rows>, or avoid n k S A <k rows> (bit masks).
// Output: shortest length (-1 if absent), visited subsets, then letter indices.
#include <algorithm>
#include <atomic>
#include <cstdint>
#include <exception>
#include <iostream>
#include <limits>
#include <mutex>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

struct Case {
  bool avoid;
  int n, k;
  uint32_t start, required;
  std::vector<std::vector<int>> rows;
};
struct Answer {
  bool found = false;
  size_t visited = 0;
  std::vector<unsigned> word;
};

Answer search(const Case &c) {
  const uint32_t count = uint32_t(1) << c.n;
  const int low_bits = std::min(c.n, 12), high_bits = c.n - low_bits;
  const uint32_t low_size = uint32_t(1) << low_bits;
  std::vector<std::vector<uint32_t>> low(c.k), high(c.k);
  for (int a = 0; a < c.k; ++a) {
    low[a].resize(low_size);
    high[a].resize(uint32_t(1) << high_bits);
    for (uint32_t s = 1; s < low_size; ++s)
      low[a][s] = low[a][s & (s - 1)] | (uint32_t(1) << c.rows[a][__builtin_ctz(s)]);
    for (uint32_t s = 1; s < high[a].size(); ++s)
      high[a][s] = high[a][s & (s - 1)] | (uint32_t(1) << c.rows[a][low_bits + __builtin_ctz(s)]);
  }
  const auto goal = [&](uint32_t s) {
    return c.avoid ? (__builtin_popcount(s) < __builtin_popcount(c.start) ||
                      (s & c.required) != c.required)
                   : (s && !(s & (s - 1)));
  };
  const uint32_t unseen = std::numeric_limits<uint32_t>::max();
  std::vector<uint32_t> parent(count, unseen), queue;
  std::vector<uint8_t> letter(count);
  parent[c.start] = c.start;
  queue.push_back(c.start);
  uint32_t end = unseen;
  if (goal(c.start)) end = c.start;
  for (size_t head = 0; head < queue.size() && end == unseen; ++head) {
    const uint32_t s = queue[head];
    for (int a = 0; a < c.k; ++a) {
      const uint32_t t = low[a][s & (low_size - 1)] | high[a][s >> low_bits];
      if (parent[t] != unseen) continue;
      parent[t] = s;
      letter[t] = static_cast<uint8_t>(a);
      queue.push_back(t);
      if (goal(t)) { end = t; break; }
    }
  }
  Answer out;
  out.visited = queue.size();
  if (end == unseen) return out;
  out.found = true;
  for (uint32_t s = end; s != c.start; s = parent[s]) out.word.push_back(letter[s]);
  std::reverse(out.word.begin(), out.word.end());
  return out;
}

int main(int argc, char **argv) {
  try {
    unsigned threads = 1;
    if (argc == 3 && std::string(argv[1]) == "--threads") {
      const std::string value = argv[2]; size_t end = 0;
      const auto parsed = std::stoul(value, &end);
      if (end != value.size() || !parsed || parsed > 64) throw std::runtime_error("threads must be 1..64");
      threads = static_cast<unsigned>(parsed);
    } else if (argc != 1) throw std::runtime_error("usage: subset_search [--threads 1..64]");
    std::vector<Case> cases;
    std::string mode;
    while (std::cin >> mode) {
      Case c{};
      if (mode != "reset" && mode != "avoid") throw std::runtime_error("expected reset or avoid");
      c.avoid = mode == "avoid";
      if (!(std::cin >> c.n >> c.k) || c.n < 1 || c.n > 24 || c.k < 1 || c.k > 256)
        throw std::runtime_error("require 1 <= n <= 24, 1 <= alphabet <= 256");
      const uint32_t full = (uint32_t(1) << c.n) - 1;
      c.start = full;
      if (c.avoid && (!(std::cin >> c.start >> c.required) || !c.start || c.start > full ||
                      !c.required || c.required > full || (c.required & c.start) != c.required ||
                      c.required == c.start)) throw std::runtime_error("require nonempty A properly contained in S");
      c.rows.assign(c.k, std::vector<int>(c.n));
      for (auto &row : c.rows) for (int &q : row)
        if (!(std::cin >> q) || q < 0 || q >= c.n) throw std::runtime_error("invalid or truncated transition row");
      cases.push_back(std::move(c));
    }
    if (cases.empty()) throw std::runtime_error("no automata supplied");
    // Dense BFS needs roughly 9*2^n bytes per active case; bound aggregate memory.
    size_t largest = 0;
    for (const auto &c : cases) largest = std::max(largest, size_t(9) << c.n);
    threads = std::min<unsigned>(threads, std::max<size_t>(1, (size_t(512) << 20) / largest));
    threads = std::min<size_t>(threads, cases.size());
    std::vector<Answer> answers(cases.size());
    std::atomic<size_t> next{0};
    std::exception_ptr failure;
    std::mutex failure_mutex;
    std::vector<std::thread> workers;
    for (unsigned t = 0; t < threads; ++t) workers.emplace_back([&] {
      try {
        for (size_t i; (i = next.fetch_add(1)) < cases.size();) answers[i] = search(cases[i]);
      } catch (...) {
        std::lock_guard<std::mutex> lock(failure_mutex);
        if (!failure) failure = std::current_exception();
        next.store(cases.size());
      }
    });
    for (auto &worker : workers) worker.join();
    if (failure) std::rethrow_exception(failure);
    for (const auto &a : answers) {
      if (a.found) std::cout << a.word.size(); else std::cout << -1;
      std::cout << ' ' << a.visited;
      for (auto letter : a.word) std::cout << ' ' << letter;
      std::cout << '\n';
    }
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n'; return 2;
  }
}
